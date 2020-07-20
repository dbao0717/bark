import React , {useEffect, useState} from 'react'

import {loadBarks} from '../lookup'

export function BarksComponent(props) {
    const textAreaRef = React.createRef()
    const [newBarks, setNewBarks] = useState([])
    const handleSubmit = (event) => {
        event.preventDefault()
        const newVal = textAreaRef.current.value
        let tempNewBarks = [...newBarks]
        tempNewBarks.unshift({
            content: newVal,
            likes: 0,
            id: 123
        })
        setNewBarks(tempNewBarks)
        textAreaRef.current.value = ''
    }
    return <div className = {props.className}>
        <div className = 'col-12 mb-3'>
            <form onSubmit = {handleSubmit}>
                <textarea ref = {textAreaRef} required = {true} className = 'form-control' name = 'tweet'>

                </textarea>
                <button type = 'submit' className = 'btn btn-primary my-3'>Bark</button>
            </form>
        </div>
        <BarksList newBarks = {newBarks}/>
    </div>
    
}

export function BarksList(props) {
    const [barksInit, setBarksInit] = useState([])
    const [barks, setBarks] = useState([])
    useEffect(() => {
        const final = [...props.newBarks].concat(barksInit)
        if(final.length !== barks.length) {
            setBarks(final)
        }
    }, [props.newBarks, barks, barksInit])
    useEffect(() => {
        const myCallback =  (response, status) => {
        if(status === 200) {
            setBarksInit(response)
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