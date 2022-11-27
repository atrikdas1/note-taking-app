import React from 'react'

function NoteList(props) {
    const editNote = (note) => {
        props.editNote(note)
    }
  return (
    <div>
        {props.notes && props.notes.map(note => {
        return(
          <div key = {note.id}>
            <p>{note.content}</p>
            <p>{note.tags}</p>

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