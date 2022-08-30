<script>
	import Calendar from "@event-calendar/core";
	import TimeGrid from "@event-calendar/time-grid";
	import DayGrid from "@event-calendar/day-grid";
	import {initializeApp, getApps, getApp} from "firebase/app";
	import {getFirestore, collection, onSnapshot, QuerySnapshot} from "firebase/firestore";

	var items = [];

	const firebaseConfig = {
		apiKey: "AIzaSyAMgh-oHI4jvo-vBsvWuB98wHYB2M3QeTA",
		authDomain: "calendar-5dc17.firebaseapp.com",
		databaseURL: "https://calendar-5dc17-default-rtdb.firebaseio.com",
		projectId: "calendar-5dc17",
		storageBucket: "calendar-5dc17.appspot.com",
		messagingSenderId: "151706105579",
		appId: "1:151706105579:web:b2e4d33f03d08dd72830ae",
		measurementId: "G-YB4GYQRF5J",
	};

	const firebaseApp = getApps().length === 0 ? initializeApp(firebaseConfig) : getApp();

	const db = getFirestore();

	const colRef = collection(db, "events");

	const data = onSnapshot(colRef, querySnapshot => {
		querySnapshot.forEach(doc => {
			var newEvent = {
				id: doc.data().id,
				title: doc.data().title,
				allDay: true,
				start: new Date(doc.data().year, doc.data().month, doc.data().day),
				end: new Date(doc.data().year, doc.data().month, doc.data().day + doc.data().len),
			};
			console.log(newEvent);
			items.push(newEvent);
			items = items;
		});
	});

	let plugins = [TimeGrid, DayGrid];
	let options = {
		view: "dayGridMonth",
		headerToolbar: {
			start: "prev,next today",
			center: "title",
			end: "dayGridMonth,timeGridWeek,timeGridDay",
		},
		events: items,
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
			<Calendar {plugins} {options} />

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
