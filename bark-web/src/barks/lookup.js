import {backEndLookup} from '../lookup'

export function apiBarkCreate(newBark, callback) {
    backEndLookup("POST", "/barks/create/", callback, {content: newBark})
  
}
 
export function apiBarkAction(barkId, action, callback) {
  const data = {id: barkId, action: action}
  backEndLookup("POST", "/barks/action/", callback, data)

}

export function apiBarkDetail(barkId, callback) {
    backEndLookup("GET", `/barks/${barkId}`, callback)
}

export function apiBarkList(username, callback) {
  let endpoint = "/barks/"
  if(username) {
      endpoint = `/barks/?username=${username}`
  }
    backEndLookup("GET", endpoint, callback)
}