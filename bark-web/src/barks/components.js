import React , {useEffect, useState} from 'react'

import {loadBarks} from '../lookup'
  
export function BarksList(props) {
    const [barks, setBarks] = useState([])

    useEffect(() => {
        const myCallback =  (response, status) => {
        if(status === 200) {
            setBarks(response)
        } else {
            alert("There was an error")
        }
        }
        loadBarks(myCallback)
    }, [])
    return barks.map((item, index)=>{
        return <Bark bark = {item} className = 'my-5 py-5 border bg-white text-dark' key = {`${index}-{item.id}`}/>
    })
}

export function ActionBtn(props) {
    const {bark, action} = props
    const [likes, setLikes] = useState(bark.likes ? bark.likes : 0)
    const [userLike, setUserLike] = useState(bark.userLike === true ? true : false)
    const className = props.className ? props.className : 'btn btn-primary btn-sm'
    const actionDisplay = action.display ? action.display : 'Action'
    const handleClick = (event) => {
        event.preventDefault()
        if(action.type === 'like') {
            if(userLike === true) {
                setLikes(likes - 1)
                setUserLike(false)
            } else {
                setLikes(likes + 1)
                setUserLike(true)
            }
        }
    }
    const display = action.type === 'like' ? `${likes} ${actionDisplay}` : actionDisplay
    return <button className = {className} onClick = {handleClick}>{display}</button>
  }
  
export function Bark(props) {
const {bark} = props
const className = props.className ? props.className : 'col-10 mx-auto col-md-6'
return <div className={className}>
    <p>{bark.id} - {bark.content}</p>
    <div className='btn btn-group'>
    <ActionBtn bark = {bark} action={{type: "like", display:"Likes"}}/>
    <ActionBtn bark = {bark} action={{type: "unlike", display:"Unlike"}}/>
    <ActionBtn bark = {bark} action={{type: "rebark", display:"Rebark"}}/>
    </div>
</div>
}