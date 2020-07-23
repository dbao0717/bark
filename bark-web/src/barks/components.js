import React , {useState, useEffect} from 'react'
import {BarksList} from './list'
import {BarkCreate} from './create'
import {apiBarkDetail} from './lookup'
import {Bark} from './detail'

export function BarksComponent(props) {
    const [newBarks, setNewBarks] = useState([])
    const canBark = props.canBark === "false" ? false : true
    const handleNewBark = (newBark) => {
        let tempNewBarks = [...newBarks]
        setNewBarks(tempNewBarks)
        tempNewBarks.unshift(newBark)
    }
    return <div className = {props.className}>
        {canBark === true && <BarkCreate didBark = {handleNewBark} className = 'col-12 mb-3' />}
        <BarksList newBarks = {newBarks} {...props}/>
    </div>
}

export function BarkDetailComponent(props) {
    const {barkId} = props
    const [didLookup, setDidLookup] = useState(false)
    const [bark, setBark] = useState(null)
    const handleBackEndLookup = (response, status) => {
        if(status === 200) {
            setBark(response)
        } else {
            alert("There was an error finding your bark.")
        }
    }
    useEffect(() => {
        if(didLookup === false) {
            apiBarkDetail(barkId, handleBackEndLookup)
            setDidLookup(true)
        }
    }, [barkId, didLookup, setDidLookup])
    return bark === null ? null : <Bark bark = {bark} className = {props.className} />
}