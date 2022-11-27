import React from 'react';
import Badge from 'react-bootstrap/Badge';
import APIService from '../components/APIService';

function NoteList(props) {

    const editNote = (note) => {
        props.editNote(note)
    }

    const deleteNote = (note) => {
        APIService.DeleteNote(note.id)
        .then(() => props.deleteNote(note))
        .catch(error => console.log(error))
    }

  return (
    <div>
        {props.notes && props.notes.map(note => {
        return(
          <div key = {note.id}>
            <div className="card fluid">
                <div className="section">
                    <p>{note.content}</p>
                </div>
                <div className="section">
                    {note.tags.map((tag, index) => <Badge style={{marginRight:"5px"}} key={index} bg="primary">{tag}</Badge>)}
                </div>
            </div>

            <div className='row'>
                <div className='col-2'>
                    <button className='btn btn-primary'
                    onClick={() => editNote(note)}>Update</button>
                </div>
                <div className='col-2'>
                    <button className='btn btn-danger'
                    onClick={() => deleteNote(note)}>Delete</button>
                </div>
            </div>
            <hr/>
          </div>
        )

      })}
    </div>
  )
}

export default NoteList