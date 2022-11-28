// This file interfaces with the backend via a proxy to receive all the responses from the backend
export default class APIService{
    static GetAll(){
        return fetch('/v1/note', {
            'method':'GET',
            headers: {
              'Content-Type':'application/json'
            },
          })
          .then(resp => resp.json())
    }

    static UpdateNote(id, body){
        var tags = body.tags
        var content = body.content
        var tags_array = tags.toString().split(',')
        var update_body = {"content": content, "tags": tags_array}
        return fetch(`/v1/note/${id}`, {
            'method':'PUT',
            headers: {
              'Content-Type':'application/json'
            },
            body: JSON.stringify(update_body)
          })
          .then(resp => resp.json())
    }

    static CreateNote(body){
        var tags = body.tags
        var content = body.content
        var tags_array = tags.toString().split(',')
        var update_body = {"content": content, "tags": tags_array}
        return fetch('/v1/note', {
            'method':'POST',
            headers: {
              'Content-Type':'application/json'
            },
            body: JSON.stringify(update_body)
          })
          .then(resp => resp.json())
    }

    static DeleteNote(id){
        return fetch(`/v1/note/${id}`, {
            'method':'DELETE',
            headers: {
              'Content-Type':'application/json'
            },
          })
    }

    static DeleteAll(){
        return fetch('/v1/note', {
            'method':'DELETE',
            headers: {
              'Content-Type':'application/json'
            },
          })
    }

    static FunnyNote(){
        return fetch('/v1/note/funny', {
            'method':'POST',
            headers: {
              'Content-Type':'application/json'
            },
          })
          .then(resp => resp.json())
    }

    static FilterTag(tag){
        return fetch(`/v1/note/tag/${tag}`, {
            'method':'GET',
            headers: {
              'Content-Type':'application/json'
            },
          })
          .then(resp => resp.json())
    }

    static FilterEntity(entity){
        return fetch(`/v1/note/entity/${entity}`, {
            'method':'GET',
            headers: {
              'Content-Type':'application/json'
            },
          })
          .then(resp => resp.json())
    }
}