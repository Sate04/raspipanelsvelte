<script>
    import Calendar from '@event-calendar/core';
    import TimeGrid from '@event-calendar/time-grid';
	import DayGrid from '@event-calendar/day-grid'

    let plugins = [TimeGrid, DayGrid];
    let options = {
        view: 'dayGridMonth',
        headerToolbar: {
            start: 'prev,next today',
            center: 'title',
            end: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
		events: [{
			id: 'birthday',
			title: 'Birthday',
			allDay: true,
			start: new Date(),
			end: new Date(),
		}

		]
    };
	


	let pagenum = 0;
</script>

<main>
	{#if pagenum == 0}
		<div class="flex justify-evenly">
			<div>
				<btn
					on:click={() => {
						pagenum = 1;
					}}>Sports</btn
				>
			</div>
			<div>
				<btn
					on:click={() => {
						pagenum = 2;
					}}>News</btn
				>
			</div>
			<div>
				<btn
					on:click={() => {
						pagenum = 3;
					}}>Cryptocurrency</btn
				>
			</div>
			<div>
				<btn
					on:click={() => {
						pagenum = 4;
					}}>Calendar</btn
				>
			</div>
		</div>
	{/if}

	{#if pagenum == 1}
		<div>
			Boo! <btn
				on:click={() => {
					pagenum = 0;
				}}>back</btn
			>
		</div>
	{/if}

	{#if pagenum == 2}
		<div>
			hey <btn
				on:click={() => {
					pagenum = 0;
				}}>back</btn
			>
		</div>
	{/if}

	{#if pagenum == 3}
		<div>
			whats up <btn
				on:click={() => {
					pagenum = 0;
				}}>back</btn
			>
		</div>
	{/if}

	{#if pagenum == 4}
		<div>

			<Calendar {plugins} {options}/>

			<btn
				on:click={() => {
					pagenum = 0;
				}}>back</btn
			>
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
