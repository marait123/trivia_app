import React, { Component } from 'react';

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
  constructor(){
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: null,
      endpoint:'/questions',
      method:'GET',
      searchTerm:''
    }
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = (page=1) => {

    $.ajax({
      type: this.state.method,
      url: `${this.state.endpoint}?page=${page}`, //TODO: update request URL
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }
  choose_questions(page){
    if(this.state.endpoint == '/questions/search'){
      this.submitSearch(this.state.searchTerm, this.state.page)
      return;
    }else if(this.state.endpoint=='/questions'){
      this.getQuestions(page);
    }
    else if(this.state.endpoint==`/categories/${this.state.currentCategory}/questions`){
      this.getByCategory(this.state.currentCategory,page);
    }
  }
  selectPage(num) {
    this.setState({page: num}, () => this.choose_questions(num));
  }

  createPagination(){
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10)
    console.log("max pages")
    console.log(maxPage)
    console.log("total questions")
    console.log(this.state.totalQuestions)
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {this.selectPage(i)}}>{i}
        </span>)
    }
    return pageNumbers;
  }

  getByCategory= (id,page=1) => {
    this.setState({endpoint:`/categories/${id}/questions`,method:"GET"})
    $.ajax({
      url: `/categories/${id}/questions?page=${page}`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  submitSearch = (searchTerm,page=1) => {
    this.setState({searchTerm:searchTerm, page:page})
    this.setState({endpoint:'/questions/search',method:"POST"})
    $.ajax({
      url: `/questions/search?page=${page}`, //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({searchTerm: searchTerm}),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  questionAction = (id) => (action) => {
    if(action === 'DELETE') {
      if(window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `/questions/${id}`, //TODO: update request URL
          type: "DELETE",
          success: (result) => {
            this.getQuestions();
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again')
            return;
          }
        })
      }
    }
  }

  render() {
    return (
      <div className="question-view">
        <div className="categories-list">
          <h2 onClick={() => {this.getQuestions()}}>Categories</h2>
          <ul>
            {Object.keys(this.state.categories).map((id, ) => (
              <li key={id} onClick={() => {this.getByCategory(this.state.categories[id].id)}}>
                {this.state.categories[id].type}
                <img alt={`fd `} className="category" src={`${this.state.categories[id].type}.svg`}/>
              </li>
            ))}
          </ul>
          <Search submitSearch={this.submitSearch}/>
        </div>
        <div className="questions-list">
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => (
            
            <Question
              type={q.type}
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={ this.state.categories[q.category]} 
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className="pagination-menu">
            {this.createPagination()}
          </div>
        </div>

      </div>
    );
  }
}

export default QuestionView;
