import React, { useState } from 'react';
import Badge from 'react-bootstrap/Badge';
import APIService from '../components/APIService';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

function NoteList(props) {

    const [show, setShow] = useState(false);
    const [noteToDelete, setNoteToDelete] = useState(null);

    const handleClose = () => setShow(false);
    const handleShow = (note) => {
      setShow(true);
      setNoteToDelete(note)
    }

    const editNote = (note) => {
        props.editNote(note)
    }

    const deleteNote = () => {
        APIService.DeleteNote(noteToDelete.id)
        .then(() => props.deleteNote(noteToDelete))
        .then(() => {
          setNoteToDelete(null)
          setShow(false)})
        .catch(error => console.log(error))
    }

    const filterTag = (tag) => {
        APIService.FilterTag(tag)
        .then(resp => props.filterByTag(resp.notes))
        .catch(error => console.log(error))
    }

    const filterEntity = (entity) => {
      APIService.FilterEntity(entity)
      .then(resp => props.filterByEntity(resp.notes))
      .catch(error => console.log(error))
  }

  return (
    <div>
        {/* Populate feed with notes if they exist */}
        {props.notes && props.notes.map(note => {
        return(
          <div key = {note.id}>
            <div className="card fluid">
                <div className="section">
                    <h5>Content</h5>
                    <p>{note.content}</p>
                </div>
                {/* Populate div with individual tags from an array */}
                <div className="section">
                    <span><b>Tags:</b>&nbsp;&nbsp;&nbsp;{note.tags.map((tag, index) => <Badge pill onClick={() => filterTag(tag)} style={{marginRight:"5px", cursor:"pointer"}} key={index} bg="primary">{tag}</Badge>)}</span>
                </div>
                <div className="section">
                  <span><b>Entities:</b>&nbsp;&nbsp;&nbsp;{note.entities.map((entity, index) => <Badge pill onClick={() => filterEntity(entity)} style={{marginRight:"5px", cursor:"pointer"}} key={index} bg="primary">{entity}</Badge>)}</span>
                </div>
                <div className='row'>
                    <div className='col-1 centre'>
                        <button className='btn btn-primary'
                        onClick={() => editNote(note)}><i className="fa fa-pencil-square"></i>
                        </button>
                    </div>
                    <div className='col-1 centre'>
                        <button className='btn btn-danger'
                        onClick={() => handleShow(note)}><i className="fa fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
            <Modal show={show} onHide={handleClose}>
              <Modal.Header closeButton>
                <Modal.Title>Delete Confirmation</Modal.Title>
              </Modal.Header>
              <Modal.Body>Are you sure you want to delete this note?</Modal.Body>
              <Modal.Footer>
                <Button variant="light" onClick={handleClose}>
                  No
                </Button>
                <Button variant="danger" onClick={deleteNote}>
                  Yes
                </Button>
              </Modal.Footer>
            </Modal>
          </div>
        )

      })}
    </div>
  )
}

export default NoteList