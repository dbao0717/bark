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

export function apiBarkFeed(callback, nextUrl) {
  let endpoint = "/barks/feed/"
  if(nextUrl !== null && nextUrl !== undefined) {
    endpoint = nextUrl.replace("http://localhost:8000/api", "")
  }
  backEndLookup("GET", endpoint, callback)
}

export function apiBarkList(username, callback, nextUrl) {
  let endpoint = "/barks/"
  if(username) {
      endpoint = `/barks/?username=${username}`
  }
  if(nextUrl !== null && nextUrl !== undefined) {
    endpoint = nextUrl.replace("http://localhost:8000/api", "")
  }
  backEndLookup("GET", endpoint, callback)
}