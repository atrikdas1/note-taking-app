import React, { useState, useEffect } from "react";
import "./App.css";
import NoteList from "./components/NoteList";
import Form from "./components/Form";
import APIService from "./components/APIService";

function App() {
	// usestate for setting a javascript
	// object for storing and using data
	const [notes, setNotes] = useState([]);
  const [editedNote, setEditedNote] = useState(null);
  const [isFilter, setIsFilter] = useState(false);

	// Using useEffect for first time rendering notes onto view
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

  // Set view after updating selected note
  const updatedData = (note) => {
    const new_note = notes.map(my_note => {
      if (my_note.id === note.id) {
        return note
      } else {
        return my_note
      }
    })
    setNotes(new_note)
    setEditedNote({content:'', tags:''})
  }

  // Set view after adding new note to the end of feed
  const createdData = (note) => {
    const new_notes = [...notes, note]
    setNotes(new_notes)
    setEditedNote({content:'', tags:''})
  }

  // Set view to show notes based on selected tag
  const filterByTag = (filtered_notes) => {
    setNotes(filtered_notes)
    setIsFilter(true)
  }

  // Remove selected note from view
  const deleteNote = (note) => {
    const new_notes = notes.filter(my_note => {
      if (my_note.id === note.id) {
        return false
      } else {
        return true
      }
    })
    setNotes(new_notes)
  }

  // Call API to generate a funny note
  const funnyNote = () => {
    APIService.FunnyNote()
    .then(resp => {
      const new_notes = [...notes, resp]
      setNotes(new_notes)})
    .catch(error => console.log(error))
  }

  // Call API to delete all notes
  const deleteAll = () => {
    APIService.DeleteAll()
    .then(() => setNotes([]))
    .catch(error => console.log(error))
  }

  // Call API to get all notes
  const getAll = () => {
    APIService.GetAll()
    .then(resp => {
      setNotes(resp.notes)
      setIsFilter(false)})
    .catch(error => console.log(error))
  }

	return (
		<div className="App">
      <div className="row">
        <div className="col-6">
          <h1>Note Taking App</h1>
        </div>
        <div className='col-2 centre'>
            <button className='btn btn-success'
            onClick={funnyNote}>Create Funny Note</button>
        </div>
        <div className='col-2 centre'>
            <button className='btn btn-danger'
            onClick={deleteAll}>Delete All</button>
        </div>
        {/* Display Reset Filter button only when tag is clicked */}
        {
          isFilter ? 
          <div className='col-2 centre'>
            <button className='btn btn-warning'
            onClick={getAll}>Reset Filter</button>
          </div> : null
        }
      </div>
			
      <div className="row">
        <div className="col-md-6">
          {/* Display Update form only if setEditedNote is filled up, else display Create form */}
          {editedNote ? <Form note={editedNote} updatedData={updatedData} createdData={createdData} setEditedNote={setEditedNote}/>
          : setEditedNote({content:'', tags:''})}
        </div>
        <div className="col-md-6">
          <NoteList notes={notes} editNote={editNote} deleteNote={deleteNote} filterByTag={filterByTag}/>
        </div>        
      </div>
		</div>
	);
}

export default App;
