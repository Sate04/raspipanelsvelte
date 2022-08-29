<script>
	let thing = 1;

	function goto(){
		thing++;
	}
</script>

<main> 
	<div class="flex justify-evenly">
		<div>
			<btn on:click={goto}>Sports</btn>
		</div>
		<div>
			<btn>News</btn>
		</div>
		<div>
			<btn>Cryptocurrency</btn>
		</div>
		<div>
			<btn>Calendar</btn>
		</div>	
	</div>
	{#if thing > 3}
	<div>
		Boo!
	</div>
	{/if}
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>