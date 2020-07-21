import {backEndLookup} from '../lookup'

export function apiBarkCreate(newBark, callback) {
    backEndLookup("POST", "/barks/create/", callback, {content: newBark})
  
  }
  
export function apiBarkList(callback) {
    backEndLookup("GET", "/barks/", callback)
}