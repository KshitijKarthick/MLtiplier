from pathlib import PosixPath

from fastai.utils.mem import *
from fastai.vision import *

# Constants
wd = 1e-3
bs, max_size = 1, (256, 256)
arch = models.resnet34
stub_dataset_path = PosixPath("stub/dataset")
model_path = PosixPath("model_resources/kkt-denoise-2b-unfrozen-ep2-minimal")

# Globals
warnings.filterwarnings("ignore")


def load_dataset(dataset_path, bs=1, max_size=max_size):
    databunch = (
        ImageImageList.from_folder(dataset_path).split_none()
            .label_from_func(lambda x: x)
            .transform(get_transforms(), size=max_size, tfm_y=True)
            .databunch(bs=bs, device='cpu')
            .normalize(imagenet_stats, do_y=True)
    )
    databunch.c = 3
    return databunch


def build_learner():
    stub_databunch = load_dataset(bs=bs, max_size=max_size, dataset_path=stub_dataset_path)
    learn = unet_learner(
        stub_databunch, arch, loss_func=F.l1_loss, blur=True, norm_type=NormType.Weight,
        pretrained=True)
    learn.load(model_path.absolute(), with_opt=False, purge=True)
    return learn


def obtain_enhanced_size(increase_resolution_percent, base_image_resolution):
    make_even = lambda num: num if num % 2 == 0 else num + 1
    enhanced_size = (
        make_even(base_image_resolution[0] + math.ceil(
            increase_resolution_percent * base_image_resolution[0] / 100.0)),
        make_even(base_image_resolution[1] + math.ceil(
            increase_resolution_percent * base_image_resolution[1] / 100.0))
    )
    return enhanced_size


def predict_with_custom_resizing(learner, image_dir_path, base_image_resolution,
                                 increase_resolution_percent=0):
    enhanced_size = obtain_enhanced_size(increase_resolution_percent=increase_resolution_percent,
                                         base_image_resolution=base_image_resolution)
    predict_dataset = (
        ImageImageList.from_folder(image_dir_path)
        .split_none()
        .label_from_func(lambda _: _)
        .transform(get_transforms(), size=enhanced_size, tfm_y=True)
        .databunch(bs=1, device='cpu').normalize(imagenet_stats, do_y=True)
    )
    predict_learner = copy(learner)
    predict_learner.data = predict_dataset
    p, img_hr, b = predict_learner.predict(predict_dataset.train_ds.x[0])
    del(predict_dataset, predict_learner)
    return Image(img_hr.clamp_(0.0, 1.0))


def resize(image, shape):
    return image.resize((3, *shape))
