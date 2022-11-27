import React from 'react';
import Badge from 'react-bootstrap/Badge';

function NoteList(props) {

    const editNote = (note) => {
        props.editNote(note)
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
                    {note.tags.map((tag, index) => <Badge key={index} bg="primary">{tag}</Badge>)}
                </div>
            </div>

            <div className='row'>
                <div className='col-md-1'>
                    <button className='btn btn-primary'
                    onClick={() => editNote(note)}>Update</button>
                </div>
                <div className='col-md-1'>
                    <button className='btn btn-danger'>Delete</button>
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