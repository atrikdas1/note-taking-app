export default class APIService{
    static UpdateNote(id, body){
        return fetch(`/v1/note/${id}`, {
            'method':'PUT',
            headers: {
              'Content-Type':'application/json'
            },
            body: JSON.stringify(body)
          })
          .then(resp => resp.json())
    }
}