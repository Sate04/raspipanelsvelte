<script>
	import Calendar from "@event-calendar/core";
	import TimeGrid from "@event-calendar/time-grid";
	import DayGrid from "@event-calendar/day-grid";
	import {initializeApp, getApps, getApp} from "firebase/app";
	import {getFirestore, collection, onSnapshot, doc, setDoc, getDoc, deleteDoc} from "firebase/firestore";
	import {DateInput} from "date-picker-svelte";
	import axios from 'axios'

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
			items.push(newEvent);
			items = items;
		});
	});

	let ec;
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

	let newTitle;
	let newStart = new Date();
	let newEnd;
	let removeName;

	let btc = cryptoUpdate();
	let eth;
	let doge;
	function cryptoUpdate() {
		if (pagenum == 3) {
			axios({
				method: 'get',
				url: 'https://api.coingecko.com/api/v3/simple/price',
				params: {
					ids: 'bitcoin,ethereum,dogecoin',
					vs_currencies: 'usd',
				}
			})
			.then(function (response) {
				btc = response.data.bitcoin.usd;
				eth = response.data.ethereum.usd;
				doge = response.data.dogecoin.usd;	
				btc = btc;
				eth = eth;
				doge = doge;
			})
		}

	}
	setInterval(cryptoUpdate, 10000);

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
						cryptoUpdate();
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
		<div class="flex flex-col justify-center">
			<div class="flex justify-evenly">
				<img alt="Sorry" src="https://bitcoin.org/img/icons/opengraph.png?1660986466" />
			</div>
			<div class="flex flex-row justify-around">
				<p>
					
				BTC: ${btc}
				
				</p>
				<p>
					
				ETH: ${eth}
					
				</p>
				<p>
					
				DOGE: ${doge}
				
				</p>
			</div>
			<div>
				<btn
				on:click={() => {
					pagenum = 0;
				}}>back</btn
				>
			</div>
		</div>
	{/if}

	{#if pagenum == 4}
		<div>
			<Calendar bind:this={ec} {plugins} {options} />
			<div class="flex flex-row">
				<div class="flex flex-col">
					<div class="w-[250px]">
						<btn
							on:click={() => {
								var newEvent = {
									id: newTitle,
									title: newTitle,
									allDay: true,
									year: newStart.getFullYear(),
									month: newStart.getMonth(),
									day: newStart.getDate(),
									len: parseInt(newEnd),
								};

								var newCalItem = {
									id: newTitle,
									title: newTitle,
									allDay: true,
									start: newStart,
									end: new Date(newStart.getFullYear(), newStart.getMonth(), newStart.getDate() + parseInt(newEnd)),
								};


								ec.addEvent(newCalItem);

								setDoc(doc(db, "events", newTitle), newEvent);
							}}
						>
							Add Event
						</btn>
					</div>
					<div class="mr-4">
						<div class="flex justify-between">
							<p>Title:</p>
							<input bind:value={newTitle} />
						</div>
						<div class="flex justify-between my-3">
							<p>Date:</p>
							<DateInput on:select={console.log(newStart)} bind:value={newStart} />
						</div>
						<div class="flex justify-between">
							<p>Length:</p>
							<input bind:value={newEnd} />
						</div>
					</div>
				</div>
				<div class="flex flex-col">
					<div>
						<btn
							on:click={() => {
								deleteDoc(doc(db, "events", removeName));

								ec.removeEventById(removeName);
							}}
						>
							Remove Event
						</btn>
					</div>
					<div>
						<div>
							Name: <input bind:value={removeName} />
						</div>
					</div>
				</div>
			</div>
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
