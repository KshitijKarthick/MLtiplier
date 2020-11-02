<script>
    // Setup tutorial https://codechips.me/sapper-with-postcss-and-tailwind/
</script>

<style lang="postcss">
  .btn {
    @apply uppercase tracking-wide font-semibold
      text-4xl px-4 py-3 shadow-lg rounded;
  }
</style>

<svelte:head>
	<title>ML Project</title>
</svelte:head>

<div class="space-y-10 text-center">
  <h1 class="text-7xl uppercase font-bold">Great success!</h1>
  <button class="btn">DO NOT PRESS THIS BUTTON!</button>
</div>