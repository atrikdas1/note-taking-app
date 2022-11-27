import React, {useState, useEffect} from 'react';
import APIService from '../components/APIService';

function Form(props) {
    const [content, setContent] = useState(props.note.content);
    const [tags, setTags] = useState(props.note.tags);

    useEffect(() => {
        setContent(props.note.content)
        setTags(props.note.tags)
    }, [props.note])
    const updateNote = () => {
        APIService.UpdateNote(props.note.id, {content, tags})
        .then(resp => props.updatedData(resp))
        .catch(error => console.log(error))
    }

    return (
        <div>
            {props.note ? (
                <div className="mb-3">
                    <label htmlFor='content' className='form-label'>Content</label>
                    <textarea onChange={(e) => setContent(e.target.value)} rows='5' value={content} className='form-control' placeholder='Please enter content'/>

                    <label htmlFor='tags' className='form-label'>Tags</label>
                    <input onChange={(e) => setTags(e.target.value)} value={tags} type="text" className='form-control' placeholder='Please enter tags'/>

                    <button onClick={updateNote} className='btn btn-success mt-3'>Update</button>
                </div>
            ):null
            }
        </div>
    )
}

export default Form