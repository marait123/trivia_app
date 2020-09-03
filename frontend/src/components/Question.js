import React, { Component } from 'react';
import '../stylesheets/Question.css';

class Question extends Component {
  props = {
    category:{
      type:'loading'
    }
  }
  constructor(){
    super();
    this.state = {
      visibleAnswer: false
    }

  }

  flipVisibility() {
    this.setState({visibleAnswer: !this.state.visibleAnswer});
  }
  componentDidMount(){
  }

  render  () {
    
    const { question, answer, category, difficulty, type } = this.props;
     try {
       type = category.type;
     } catch (error) {
      //  console.log(category)
     }
     return (
      <div className="Question-holder">
        <div className="Question">{question}</div>
        <div className="Question-status">
          <img className="category" src={`${type}.svg`}/>
          <div className="difficulty">Difficulty: {difficulty}</div>
          <img src="delete.png" className="delete" onClick={() => this.props.questionAction('DELETE')}/>
          
        </div>
        <div className="show-answer button"
            onClick={() => this.flipVisibility()}>
            {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
          </div>
        <div className="answer-holder">
          <span style={{"visibility": this.state.visibleAnswer ? 'visible' : 'hidden'}}>Answer: {answer}</span>
        </div>
      </div>
    );
  }
}

export default Question;
