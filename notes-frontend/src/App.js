import React, { useState, useEffect } from "react";
import "./App.css";
import NoteList from "./components/NoteList";
import Form from "./components/Form";
import APIService from "./components/APIService";
import Navbar from 'react-bootstrap/Navbar';
import Container from 'react-bootstrap/Container';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

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
  const updatedData = (resp) => {
    // Call GetAll notes here because the view is reset so that the 
    // modified note comes on top
    APIService.GetAll()
    .then(res => {
      setNotes(res.notes)
      setIsFilter(false)
      setEditedNote({content:'', tags:''})})
    .then(window.scrollTo(0, 0))
    .catch(error => console.log(error))
  }

  // Set view after adding new note to the start of feed
  const createdData = (note) => {
    const new_notes = [note, ...notes]
    setNotes(new_notes)
    setEditedNote({content:'', tags:''})
  }

  // Set view to show notes based on selected tag
  const filterByTag = (filtered_notes) => {
    setNotes(filtered_notes)
    setIsFilter(true)
  }

  // Set view to show notes based on selected entity
  const filterByEntity = (filtered_notes) => {
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
      const new_notes = [resp, ...notes]
      setNotes(new_notes)})
    .catch(error => console.log(error))
  }

  // Call API to delete all notes
  const deleteAll = () => {
    APIService.DeleteAll()
    .then(() => setNotes([]))
    .then(setShow(false))
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

  const [show, setShow] = useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);



  const [fixedDivWidth, setFixedDivWidth] = useState(undefined);
  const [fixedDivTop, setFixedDivTop] = useState(undefined);

  useEffect(() => {
    const fixedDivEl = document.querySelector('.fixeddiv').getBoundingClientRect();
    setFixedDivWidth(fixedDivEl.width);
    setFixedDivTop(fixedDivEl.top);
  }, []);

  useEffect(() => {
    if (!fixedDivTop) return;
  
    window.addEventListener('scroll', isSticky);
    return () => {
      window.removeEventListener('scroll', isSticky);
    };
  }, [fixedDivTop]);
  
  const isSticky = (e) => {
    const fixedDivEl = document.querySelector('.fixeddiv');
    const scrollTop = window.scrollY;
    if (scrollTop >= fixedDivTop - 70) {
      fixedDivEl.classList.add('is-sticky');
    } else {
      fixedDivEl.classList.remove('is-sticky');
    }
  }

	return (
		<div className="App">
      <Navbar bg="light" fixed="top">
        <Container>
            <Navbar.Brand>
              <h2>Note Taking App</h2>
            </Navbar.Brand>
        </Container>
        <div className='col-2 centre'>
            <button className='btn btn-success'
            onClick={funnyNote}>Create Funny Note</button>
        </div>
        <div className='col-2 centre'>
            <button className='btn btn-danger'
            onClick={handleShow}>Delete All</button>
        </div>
        {/* Display Reset Filter button only when tag is clicked */}
        {
          isFilter ? 
          <div className='col-2 centre'>
            <button className='btn btn-warning'
            onClick={getAll}>Reset Filter</button>
          </div> : null
        }
      </Navbar>

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Delete All Confirmation</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          Are you sure you want to delete all the notes in the database?
          This action is not reversible.
        </Modal.Body>
        <Modal.Footer>
          <Button variant="light" onClick={handleClose}>
            No
          </Button>
          <Button variant="danger" onClick={deleteAll}>
            Yes
          </Button>
        </Modal.Footer>
      </Modal>
			
      <div className="row">
        <div className="col-md-6">
          <div className="fixeddiv" style={{width : fixedDivWidth}}>
            {/* Display Update form only if setEditedNote is filled up, else display Create form */}
            {editedNote ? <Form note={editedNote} updatedData={updatedData} createdData={createdData} setEditedNote={setEditedNote}/>
            : setEditedNote({content:'', tags:''})}
          </div>
        </div>
        <div className="col-md-6">
          <NoteList notes={notes} editNote={editNote} deleteNote={deleteNote} filterByTag={filterByTag} filterByEntity={filterByEntity}/>
        </div>        
      </div>
		</div>
	);
}

export default App;
