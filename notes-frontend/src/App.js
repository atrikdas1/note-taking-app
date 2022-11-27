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

  const createdData = (note) => {
    const new_notes = [...notes, note]
    setNotes(new_notes)
  }

  const openForm = () => {
    setEditedNote({content:'', tags:''})
  }

	return (
		<div className="App">
      <div className="row">
        <div className="col">
          <h1>Note Taking App</h1>
        </div>
        <div className="col">
          <button className="btn btn-success" onClick={openForm}>Insert Note</button>
        </div>
      </div>
			
        <NoteList notes={notes} editNote={editNote}/>
        {editedNote ? <Form note={editedNote} updatedData={updatedData} createdData={createdData}/> : null}
        
		</div>
	);
}

export default App;
