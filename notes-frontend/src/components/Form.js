import React, {useState, useEffect} from 'react';
import APIService from '../components/APIService';
import Alert from 'react-bootstrap/Alert';

function Form(props) {
    const [content, setContent] = useState(props.note.content);
    const [tags, setTags] = useState(props.note.tags);
    const [entities, setEntities] = useState(props.note.entities);
    const [showAlert, setShowAlert] = useState(false);

    // Switch to create form if clicked cancel
    const openForm = () => {
        props.setEditedNote({content:'', tags:''})
    }

    useEffect(() => {
        setContent(props.note.content)
        setTags(props.note.tags)
        setEntities(props.note.entities)
    }, [props.note])

    // If required fields are empty, display alert. Else, call API to update note
    const updateNote = () => {   
        if (content == "" || tags == ""){
            setShowAlert(true)
        } else{     
            APIService.UpdateNote(props.note.id, {content, tags})
            .then(resp => props.updatedData(resp))
            .catch(error => console.log(error))
        }
    }

    // If required fields are empty, display alert. Else, call API to create note
    const createNote = () => {
        if (content == "" || tags == ""){
            setShowAlert(true)
        } else{
            APIService.CreateNote({content, tags})
            .then(resp => props.createdData(resp))
            .catch(error => console.log(error))
        }
    }

    return (
        <div>
            {/* Only show alert if showAlert is true */}
            {
                showAlert ?
                <Alert variant="danger" onClose={() => setShowAlert(false)} dismissible>
                    Please change your input and try again.
                </Alert>
                : null
            }
            {props.note ? (
                <div className="mb-3 card-light">
                    <div>
                        <label htmlFor='content' className='form-label'>Content</label>
                        <textarea onChange={(e) => setContent(e.target.value)} rows='5' value={content} className='form-control' placeholder='Please enter content'/>
                    </div>

                    <div>
                        <label htmlFor='tags' className='form-label'>Tags</label>
                        <input onChange={(e) => setTags(e.target.value)} value={tags} type="text" className='form-control' placeholder='Please enter tags separated by commas'/>
                    </div>
                    
                    {/* Change buttons from Create to Update based on if note ID is passed as a prop */}
                    {
                        props.note.id ? 
                        <div className='row'>
                            <div className='col-2'>
                                <button onClick={updateNote} className='btn btn-success mt-3'>Update</button>
                            </div>
                            <div className='col-2'>
                                <button onClick={openForm} className='btn btn-danger mt-3'>Cancel</button>
                            </div>
                        </div>
                        : 
                        <div className='row'>
                            <div className='col-2'>
                                <button onClick={createNote} className='btn btn-success mt-3'>Create</button>
                            </div>
                        </div>
                    }
                </div>
            ):null
            }
        </div>
    )
}

export default Form