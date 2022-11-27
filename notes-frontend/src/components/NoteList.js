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

    const filterTag = (tag) => {
        APIService.FilterTag(tag)
        .then(resp => props.filterByTag(resp.notes))
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
                    {note.tags.map((tag, index) => <Badge pill onClick={() => filterTag(tag)} style={{marginRight:"5px", cursor:"pointer"}} key={index} bg="primary">{tag}</Badge>)}
                </div>
                <div className='row'>
                    <div className='col-2 centre'>
                        <button className='btn btn-primary'
                        onClick={() => editNote(note)}>Update</button>
                    </div>
                    <div className='col-2 centre'>
                        <button className='btn btn-danger'
                        onClick={() => deleteNote(note)}>Delete</button>
                    </div>
                </div>
            </div>
          </div>
        )

      })}
    </div>
  )
}

export default NoteList