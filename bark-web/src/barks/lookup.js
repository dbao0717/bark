import {backEndLookup} from '../lookup'

export function apiBarkCreate(newBark, callback) {
    backEndLookup("POST", "/barks/create/", callback, {content: newBark})
  
}
 
export function apiBarkAction(barkId, action, callback) {
  const data = {id: barkId, action: action}
  backEndLookup("POST", "/barks/action/", callback, data)

}

export function apiBarkList(callback) {
    backEndLookup("GET", "/barks/", callback)
}