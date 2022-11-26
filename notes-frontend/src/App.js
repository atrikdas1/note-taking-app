// Importing modules
import React, { useState, useEffect } from "react";
import "./App.css";
import axios from 'axios';

function App() {
	// usestate for setting a javascript
	// object for storing and using data
	const [data, setdata] = useState({
		name: "",
		age: 0,
		date: "",
		programming: "",
	});

	// Using useEffect for single rendering
	useEffect(() => {
		// Using fetch to fetch the api from
		// flask server it will be redirected to proxy
		axios.get("/v1/note").then((res) =>
			res.json().then((data) => {
				// Setting a data from api
				setdata({
					content: data.content,
					tags: data.tags,
				});
			})
		);
	}, []);

	return (
		<div className="App">
			<header className="App-header">
				<h1>React and flask</h1>
				{/* Calling a data from setdata for showing */}
				<p>{data.content}</p>
				<p>{data.tags}</p>

			</header>
		</div>
	);
}

export default App;
