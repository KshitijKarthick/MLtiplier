<script>
	import Nav from '../components/Nav.svelte';
	import TailwindGlobalStyle from '../components/TailwindGlobalStyle.svelte'
	export let segment;
</script>

<style>
	main {
		background-color: white;
		padding: 2em;
		margin: 0 auto;
		box-sizing: border-box;
	}
</style>

<Nav {segment}/>
<TailwindGlobalStyle />
<main>
	<div class="container mx-auto">
		<slot></slot>
	</div>
</main>