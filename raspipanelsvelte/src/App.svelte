<script>
	let pagenum = 0;

	function setpageone(){
		pagenum = 1;
	}
	function setpagetwo(){
		pagenum = 2;
	}
	function setpagethree(){
		pagenum = 3;
	}
	function setpagefour(){
		pagenum = 4;
	}
</script>

<main> 
	<div class="flex justify-evenly">
		<div>
			<btn on:click={setpageone}>Sports</btn>
		</div>
		<div>
			<btn on:click={setpagetwo}>News</btn>
		</div>
		<div>
			<btn on:click={setpagethree}>Cryptocurrency</btn>
		</div>
		<div>
			<btn on:click={setpagefour}>Calendar</btn>
		</div>	
	</div>
	{#if pagenum == 1}
	<div>
		Boo!
	</div>
	{/if}
	{#if pagenum == 2}
	<div>
		hey
	</div>
	{/if}
	{#if pagenum == 3}
	<div>
		whats up
	</div>
	{/if}
	{#if pagenum == 4}
	<div>
		hi :0
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