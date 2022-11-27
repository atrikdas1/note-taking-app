// Importing modules
import React, { useState, useEffect } from "react";
import "./App.css";
import NoteList from "./components/NoteList";
import Form from "./components/Form";

function App() {
	// usestate for setting a javascript
	// object for storing and using data
	const [notes, setNotes] = useState([]);
  const [editedNote, setEditedNote] = useState(null);

	// Using useEffect for single rendering
	useEffect(() => {
		// Using fetch to fetch the api from
		// flask server it will be redirected to proxy
		fetch("/v1/note", {
      'method':'GET',
      headers: {
        'Content-Type':'application/json'
      }
    })
    .then(resp => resp.json())
    .then(resp => setNotes(resp.notes))
    .catch(error => console.log(error))
	}, []);

  const editNote = (note) => {
    setEditedNote(note)
  }

  const updatedData = (note) => {
    const new_note = notes.map(my_note => {
      if (my_note.id === note.id) {
        return note
      } else {
        return my_note
      }
    })
    setNotes(new_note)
  }

	return (
		<div className="App">
			<h1>Note Taking App</h1>
        <NoteList notes={notes} editNote={editNote}/>
        {editedNote ? <Form note={editedNote} updatedData={updatedData}/> : null}
        
		</div>
	);
}

export default App;
