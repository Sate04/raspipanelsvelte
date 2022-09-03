<script>
	import Calendar from "@event-calendar/core";
	import TimeGrid from "@event-calendar/time-grid";
	import DayGrid from "@event-calendar/day-grid";
	import {initializeApp, getApps, getApp} from "firebase/app";
	import {getFirestore, collection, onSnapshot, doc, setDoc, deleteDoc} from "firebase/firestore";
	import {DatePicker} from "date-picker-svelte";
	import axios from "axios";
	import {Button, TextField, MaterialApp, Tabs, Tab, TabContent, Switch, Radio} from "svelte-materialify";

	let theme = "light";

	let items = [];

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

	let options = {
		view: "dayGridMonth",
		headerToolbar: {
			start: "prev,next today",
			center: "title",
			end: "dayGridMonth,timeGridWeek,timeGridDay",
		},
		events: items,
	};

	let rerender = false;

	const data = onSnapshot(colRef, querySnapshot => {
		rerender = false;
		querySnapshot.forEach(doc => {
			if (doc.data().allDay) {
				var newEvent = {
					id: doc.data().id,
					title: doc.data().title,
					allDay: true,
					start: new Date(doc.data().year, doc.data().month, doc.data().day),
					end: new Date(doc.data().year, doc.data().month, doc.data().day + doc.data().len),
				};
				items.push(newEvent);
			} else {
				var newEvent = {
					id: doc.data().id,
					title: doc.data().title,
					allDay: false,
					start: new Date(doc.data().year, doc.data().month, doc.data().day, doc.data().starthour, doc.data().startminute),
					end: new Date(doc.data().year, doc.data().month, doc.data().day, doc.data().endhour, doc.data().endminute),
				};

				items.push(newEvent);
			}
		});
		rerender = true;
	});

	let group = 1;

	let ec;
	let plugins = [TimeGrid, DayGrid];

	let cryptoids = [80, 90, 2];

	let newTitle;
	let newStart = new Date();
	let newEnd;
	let newEndTime;

	let newStartTime;

	let removeName;
	let allDay = true;

	let results = [];
	let articles = [];
	axios({
		method: "get",
		url: "https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty",
	}).then(function (response) {
		results = response.data;
		results = results.slice(0, 15);
		results = results;
		results.forEach(article => {
			axios.get(`https://hacker-news.firebaseio.com/v0/item/${article}.json?print=pretty`).then(response => {
				articles.push(response.data);
			});
		});
	});

	let newsHeadlines = [];

	const newsOptions = {
		method: "GET",
		url: "https://bing-news-search1.p.rapidapi.com/news",
		params: {safeSearch: "Off", textFormat: "Raw"},
		headers: {
			"X-BingApis-SDK": "true",
			"X-RapidAPI-Key": "05bd952bb4msh67835f4b906300dp1b8e75jsn687a13b64ecb",
			"X-RapidAPI-Host": "bing-news-search1.p.rapidapi.com",
		},
	};
	if (false) {
		axios.request(newsOptions).then(function (response) {
			newsHeadlines = response.data.value;
			newsHeadlines = newsHeadlines
				.filter(article => {
					return article.image != null;
				})
				.slice(0, 15);
		});
	}

	function parseTime(time, part) {
		switch (part) {
			case "hour":
				if (time.length == 3) {
					return parseInt(time.substring(0, 1));
				} else {
					return parseInt(time.substring(0, 2));
				}
			case "minute":
				if (time.length == 3) {
					return parseInt(time.substring(1, 3));
				} else {
					return parseInt(time.substring(2, 4));
				}
		}
	}

	let images = [];

	const imageRef = collection(db, "links");

	const imageData = onSnapshot(imageRef, querySnapshot => {
		querySnapshot.forEach(doc => {
			images.push(atob(doc.data().link));
			images = images;
		});
	});

	async function getESPN(league) {
		let nfldata = [];
		let eventdata = [];
		return new Promise(async resolve => {
			let response = await axios.get(league);
			nfldata = response.data.items;
			let nflsize = nfldata.length;
			nfldata.forEach(async item => {
				let eventresponse = await axios.get(item.$ref);
				console.log(eventresponse.data);
				nflsize--;
				eventdata.push(eventresponse.data);
				if (nflsize == 0) {
					resolve(eventdata);
				}
			});
		});
	}

	function getLink(link) {
		return axios.get(link);
	}

	function getWeekday(day) {
		switch (day) {
			case 1:
				return "Monday";
			case 2:
				return "Tuesday";
			case 3:
				return "Wednesday";
			case 4:
				return "Thursday";
			case 5:
				return "Friday";
			case 6:
				return "Saturday";
			case 0:
				return "Sunday";
		}
	}
</script>

<MaterialApp {theme}>
	<main>
		<Tabs centerActive>
			<div slot="tabs">
				<Tab>Sports</Tab>
				<Tab>News</Tab>
				<Tab>Cryptocurrency</Tab>
				<Tab>Calendar</Tab>
				<Tab>Images</Tab>
			</div>
			<div>
				<TabContent>
					<!--SPORTS-->
					<div class="d-flex justify-space-around my-2">
						<Radio bind:group value={1}>NFL</Radio>
						<Radio bind:group value={2}>MLB</Radio>
						<Radio bind:group value={3}>NHL</Radio>
						<Radio bind:group value={4}>NBA</Radio>
					</div>
					{#if group == 1}
						{#await getESPN("https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events") then events}
							<div class="grid grid-flow-col grid-rows-4 gap-3 mt-4">
								{#each events as event}
									<div class="flex flex-col border-4 p-2">
										<p class="font-bold">{event.name}</p>
										<div class="flex flex-row justify-evenly">
											{#await getLink(event.competitions[0].competitors[1].team.$ref) then team}
												<img class="h-24" src={team.data.logos[0].href} />
											{/await}
											{#await getLink(event.competitions[0].competitors[0].team.$ref) then team}
												<img class="h-24" src={team.data.logos[0].href} />
											{/await}
										</div>

										{#if event.competitions[0].boxscoreAvailable}
											<p class="text-3xl">
												{#await getLink(event.competitions[0].competitors[1].score.$ref) then score}
													{score.data.value}
												{/await}
												—
												{#await getLink(event.competitions[0].competitors[0].score.$ref) then score}
													{score.data.value}
												{/await}
											</p>
										{:else}
											<p class="mt-2">
												Game Starts:&nbsp;&nbsp;&nbsp;<span class="font-bold">{getWeekday(new Date(event.competitions[0].date).getDay())}</span>
												<span class="font-bold"
													>{new Date(event.competitions[0].date)
														.toLocaleTimeString()
														.substring(0, new Date(event.competitions[0].date).toLocaleTimeString().indexOf("PM") - 4)} PM</span
												>
											</p>
										{/if}
									</div>
								{/each}
							</div>
						{/await}
					{:else if group == 2}
						{#await getESPN("https://sports.core.api.espn.com/v2/sports/baseball/leagues/mlb/events") then events}
							<div class="grid grid-flow-col grid-rows-4 gap-3 mt-4">
								{#each events as event}
									<div class="flex flex-col border-4 p-2">
										<p class="font-bold">{event.name}</p>
										<div class="flex flex-row justify-evenly">
											{#await getLink(event.competitions[0].competitors[1].team.$ref) then team}
												<img class="h-24" src={team.data.logos[0].href} />
											{/await}
											{#await getLink(event.competitions[0].competitors[0].team.$ref) then team}
												<img class="h-24" src={team.data.logos[0].href} />
											{/await}
										</div>

										{#if event.competitions[0].boxscoreAvailable}
											<p class="text-3xl">
												{#await getLink(event.competitions[0].competitors[1].score.$ref) then score}
													{score.data.value}
												{/await}
												—
												{#await getLink(event.competitions[0].competitors[0].score.$ref) then score}
													{score.data.value}
												{/await}
											</p>
										{:else}
											<p class="mt-2">
												Game Starts:&nbsp;&nbsp;&nbsp;<span class="font-bold">{getWeekday(new Date(event.competitions[0].date).getDay())}</span>
												<span class="font-bold"
													>{new Date(event.competitions[0].date)
														.toLocaleTimeString()
														.substring(0, new Date(event.competitions[0].date).toLocaleTimeString().indexOf("PM") - 4)} PM</span
												>
											</p>
										{/if}
									</div>
								{/each}
							</div>
						{/await}
					{:else if group == 3}
						{#await getESPN("https://sports.core.api.espn.com/v2/sports/hockey/leagues/nhl/events") then events}
							<div class="grid grid-flow-col grid-rows-4 gap-3 mt-4">
								{#each events as event}
									<div class="flex flex-col border-4 p-2">
										<p class="font-bold">{event.name}</p>
										<div class="flex flex-row justify-evenly">
											{#await getLink(event.competitions[0].competitors[1].team.$ref) then team}
												<img class="h-24" src={team.data.logos[0].href} />
											{/await}
											{#await getLink(event.competitions[0].competitors[0].team.$ref) then team}
												<img class="h-24" src={team.data.logos[0].href} />
											{/await}
										</div>

										{#if event.competitions[0].boxscoreAvailable}
											<p class="text-3xl">
												{#await getLink(event.competitions[0].competitors[1].score.$ref) then score}
													{score.data.value}
												{/await}
												—
												{#await getLink(event.competitions[0].competitors[0].score.$ref) then score}
													{score.data.value}
												{/await}
											</p>
										{:else}
											<p class="mt-2">
												Game Starts:&nbsp;&nbsp;&nbsp;<span class="font-bold">{getWeekday(new Date(event.competitions[0].date).getDay())}</span>
												<span class="font-bold"
													>{new Date(event.competitions[0].date)
														.toLocaleTimeString()
														.substring(0, new Date(event.competitions[0].date).toLocaleTimeString().indexOf("PM") - 4)} PM</span
												>
											</p>
										{/if}
									</div>
								{/each}
							</div>
						{/await}
					{:else if group == 4}
						{#await getESPN("https://sports.core.api.espn.com/v2/sports/basketball/leagues/nba/events") then events}
							<div class="grid grid-flow-col grid-rows-4 gap-3 mt-4">
								{#each events as event}
									<div class="flex flex-col border-4 p-2">
										<p class="font-bold">{event.name}</p>
										<div class="flex flex-row justify-evenly">
											{#await getLink(event.competitions[0].competitors[1].team.$ref) then team}
												<img class="h-24" src={team.data.logos[0].href} />
											{/await}
											{#await getLink(event.competitions[0].competitors[0].team.$ref) then team}
												<img class="h-24" src={team.data.logos[0].href} />
											{/await}
										</div>

										{#if event.competitions[0].boxscoreAvailable}
											<p class="text-3xl">
												{#await getLink(event.competitions[0].competitors[1].score.$ref) then score}
													{score.data.value}
												{/await}
												—
												{#await getLink(event.competitions[0].competitors[0].score.$ref) then score}
													{score.data.value}
												{/await}
											</p>
										{:else}
											<p class="mt-2">
												Game Starts:&nbsp;&nbsp;&nbsp;<span class="font-bold">{getWeekday(new Date(event.competitions[0].date).getDay())}</span>
												<span class="font-bold"
													>{new Date(event.competitions[0].date)
														.toLocaleTimeString()
														.substring(0, new Date(event.competitions[0].date).toLocaleTimeString().indexOf("PM") - 4)} PM</span
												>
											</p>
										{/if}
									</div>
								{/each}
							</div>
						{/await}
					{/if}
				</TabContent>

				<TabContent>
					<!--NEWS-->
					<div>
						<div class="flex flex-col flex-center">
							<h1>Top Headlines</h1>
							<div class="grid grid-flow-row grid-cols-3 gap-8 mx-[20%]">
								{#each newsHeadlines as article}
									<div class="flex flex-col flex-center">
										<img class="h-48" src={article.image.thumbnail.contentUrl} />
										<a href={article.url} class="font-bold">{article.name}</a>
										<p class="text-left">{article.description}</p>
									</div>
								{/each}
							</div>
							<h1>Hacker News</h1>
							<div class="grid grid-flow-row grid-cols-3 gap-4">
								{#each articles as article}
									<div>
										<a href={article.url} class="font-bold">{article.title}</a>
									</div>
								{/each}
							</div>
							<img class="h-[300px]" src="https://i.kym-cdn.com/photos/images/original/002/237/978/0d1.jpg" />
						</div>
					</div>
				</TabContent>

				<TabContent>
					<!--CRYPTO-->
					<div class="flex flex-col justify-center">
						<div class="flex justify-evenly">
							<img alt="Sorry" src="https://bitcoin.org/img/icons/opengraph.png?1660986466" />
						</div>
						<div class="flex flex-row justify-evenly">
							{#each cryptoids as coin}
								<div>
									{#await getLink(`https://api.coinlore.net/api/ticker/?id=${coin}`) then response}
										{response.data[0].name}: ${response.data[0].price_usd}
									{/await}
								</div>
							{/each}
						</div>
					</div>
				</TabContent>

				<TabContent>
					<!--CALENDAR-->
					{#if rerender}
						<div>
							<Calendar bind:this={ec} {plugins} {options} />
							<div class="flex flex-row">
								<div class="flex flex-col">
									<div class="w-[250px]">
										<Button
											class="my-4"
											on:click={() => {
												if (allDay) {
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
												} else {
													var newEvent = {
														id: newTitle,
														title: newTitle,
														allDay: false,
														year: newStart.getFullYear(),
														month: newStart.getMonth(),
														day: newStart.getDate(),
														starthour: parseTime(newStartTime, "hour"),
														startminute: parseTime(newStartTime, "minute"),
														endhour: parseTime(newEndTime, "hour"),
														endminute: parseTime(newEndTime, "minute"),
													};

													var newCalItem = {
														id: newTitle,
														title: newTitle,
														allDay: false,
														start: new Date(
															newStart.getFullYear(),
															newStart.getMonth(),
															newStart.getDate(),
															parseTime(newStartTime, "hour"),
															parseTime(newStartTime, "minute")
														),
														end: new Date(newStart.getFullYear(), newStart.getMonth(), newStart.getDate(), parseTime(newEndTime, "hour"), parseTime(newEndTime, "minute")),
													};

													ec.addEvent(newCalItem);

													setDoc(doc(db, "events", newTitle), newEvent);
												}
											}}
										>
											Add Event
										</Button>
									</div>
									<div class="mr-4">
										<div class="flex justify-between">
											<TextField outlined bind:value={newTitle}>Title</TextField>
										</div>
										<div class="flex justify-between mt-4">
											All Day Event
											<Switch bind:checked={allDay} />
										</div>
										<div class="flex justify-between my-4">
											<DatePicker on:select={console.log(newStart)} bind:value={newStart} />
										</div>

										{#if !allDay}
											<div class="flex justify-between my-4">
												<TextField outlined bind:value={newStartTime}>Start Time</TextField>
											</div>
											<div class="flex justify-between mb-8">
												<TextField outlined bind:value={newEndTime}>End Time</TextField>
											</div>
										{:else}
											<div class="flex justify-between">
												<TextField outlined bind:value={newEnd}>Length</TextField>
											</div>
										{/if}
									</div>
								</div>
								<div class="flex flex-col">
									<div>
										<Button
											class="my-4"
											on:click={() => {
												deleteDoc(doc(db, "events", removeName));

												ec.removeEventById(removeName);
											}}
										>
											Remove Event
										</Button>
									</div>
									<div>
										<div>
											<TextField outlined bind:value={removeName}>Title</TextField>
										</div>
									</div>
								</div>
							</div>
						</div>
					{/if}
				</TabContent>

				<TabContent>
					<div class="grid grid-flow-col grid-cols-3 gap-4">
						{#each images as image}
							<div class="flex flex-col flex-center">
								<img class="" src={image} />
							</div>
						{/each}
					</div>
					<!--IMAGES-->
				</TabContent>
			</div>
		</Tabs>
	</main>
</MaterialApp>

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
