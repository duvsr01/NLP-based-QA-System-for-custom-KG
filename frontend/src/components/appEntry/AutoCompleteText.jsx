import React,{Component} from "react";
import './AutoCompleteText.css';

class AutoCompleteText extends Component{
    constructor(props){
        super(props);
        this.items=[
            'David',
            'Damien',
            'Sara',
            'Jane',
            'Sruthi',
            'Sakshi',
            'Shivangi',
            'Vini'
        ];
        this.state={
            suggestions: [],
            text:'',
        };
    }

    onTextChanged = (e) =>{
        const value = e.target.value;
        let suggestions = [];
        if(value.length>0){
            const regex = new RegExp(`^${value}`,'i');
             suggestions = this.items.sort().filter(v => regex.test(v));
         
        }
        this.setState(()=>({
            suggestions,
            text:value
        }));
    }
        
    suggestionSelected (value){
        this.setState(()=>({
            text:value,
            suggestions:[],
        }))
    }  


    render(){
        let displaySuggestions;
        const {suggestions,text} =  this.state;
        if(suggestions.length === 0){
            displaySuggestions= null;
        }
        else{
            displaySuggestions= (
                <ul className="AutoCompleteText" >
                {suggestions.map((item)=>         
                <li className="AutoCompleteText" onClick={()=>this.suggestionSelected(item)}>{item}</li>)}
            </ul>

            );
        }

        return(
            <div>
            <input className="AutoCompleteText" value={text} onChange={this.onTextChanged} type="text" />
              {displaySuggestions}
            </div>
        )
    }
}



export default AutoCompleteText;