function ParentModals(props){
  let body1 = <p>Test</p>;
  return (
    <div>
      <AllowanceModal modalname='addChild' header='Add Child' modalbody={ body1 } />
      <AllowanceModal modalname='removeChild' header='Remove Child' modalbody="..." />
      <AllowanceModal modalname='prCode' header='Parent Registration Code'  modalbody="..." />
      <AllowanceModal modalname='changePW' header='Change Password' modalbody="..." />
    </div>
  );
}



function ParentNavBar(props) {
  let link = $('#parent').data('link');
  let navBody = (
    <div>
      <ul className='navbar-nav mr-auto'>
        <NavModalTrigger modallabel='#addChildModal' itemlabel='Add Child' />
        <NavModalTrigger modallabel='#removeChildModal' itemlabel='Remove Child' />
        <NavModalTrigger modallabel='#prCodeModal' itemlabel='Parent Registration Code' />
        <NavModalTrigger modallabel='#changePWModal' itemlabel='Change Password' />
      </ul>
      <ul className='navbar-nav'>
        <li className='nav-item'>
          <a className='nav-link' href='/allowance/logout?next=/allowance/login'>Logout</a>
        </li>
      </ul>
    </div>
  );
  let classes = 'navbar-dark bg-info';
  return (
    <AllowanceNavBar classes={ classes } body={ navBody } />
  );
}

function Welcome(props) {
  let parentName = $('#parent').data('user').firstName;
  return (
    <h2 style={{ textAlign : 'center' }}>Welcome { parentName }</h2>
  );
}

class ChildInfo extends React.Component {
  constructor(props) {
    super(props);
  }

  clearModal(){
    $('#balChangeError').collapse('hide');
    $('#reasonError').collapse('hide');
    $('#amount').val('');
    $('#reason').val('');
  }

  render(){
    let target = "collapse" + this.props.info.childNum;
    let name = this.props.info.childName;
    let heading = "heading" + this.props.info.childNum;
    let navBody = (
      <div>
        <ul className='navbar-nav mr-auto' data-username={ this.props.info.username }>
          <NavModalTrigger modallabel='#WDModal' itemlabel='Withdraw' onClick={ () => this.clearModal() }/>
          <NavModalTrigger modallabel='#WDModal' itemlabel='Deposit' onClick={ () => this.clearModal() }/>
          <NavModalTrigger modallabel='#histModal' itemlabel='History' onClick={ this.props.histClick }/>
        </ul>
        <ul className='navbar-nav'>
          <li className='nav-item'>
            ${ this.props.info.balance.toFixed(2) }
          </li>
        </ul>

      </div>
    );
    return (
      <div className="card">
        <div className="card-header p-0" id={ heading }>
          <h2 className="mb-0">
            <button className="btn btn-info btn-lg btn-block mb-0 shadow-none collapsed"
                    type="button" data-toggle="collapse" data-target={ "#" + target }
                    aria-expanded="false" aria-controls={ target } onClick={ this.props.onClick }>
              { name }
            </button>
          </h2>
        </div>

        <div id={ target } className="collapse" aria-labelledby={ heading } data-parent="#childrenAccounts">
          <div className="card-body p-0">
            <AllowanceNavBar classes='nav-light' body={ navBody } />
          </div>
        </div>
      </div>
    );
  }
}

class Children extends React.Component {
  constructor(props) {
    super(props);
    this.currChild = '';
    this.histRef = React.createRef();
    let children = $('#parent').data('children');
    for (var child in children){
      children[child].balance = parseFloat(children[child].balance);
    }
    this.state = children;
  }

  setCurrChild(child){
    this.currChild = child;
  }

  buildHistTable(uname){
    this.histRef.current.buildTable(uname);
  }

  changeBalance(){
    let newState = this.state;
    let amount = parseFloat($('#amount').val());
    let reason = $('#reason').val();
    if(isNaN(amount)){
      $('#balChangeError').collapse('show');
    }
    else{
      $('#balChangeError').collapse('hide');
    }
    if(reason === ''){
      $('#reasonError').collapse('show');
    }
    else{
      $('#reasonError').collapse('hide');
    }
    if(!isNaN(amount) && reason !== ''){
      if($('#WDLabel').html() === 'Deposit'){
        newState[this.currChild].balance += amount;
      }
      else{
        newState[this.currChild].balance -= amount;
      }
      this.setState(newState);
      let postInfo = {
        username : this.currChild,
        rsn : reason,
        amt: amount,
        type: $('#WDLabel').html()
      };
      $.post('/allowance/update/', postInfo);
      $('#WDModal').modal('hide');
    }
  }

  render(){
    let childInfoElements = [];
    let i = 1;
    let histModalBody = ( <AllowanceHistTable ref={ this.histRef } child={ Object.keys(this.state)[0] }/> );
    let WDModalBody = (
      <form>
        <p className='border border-danger rounded p-2 text-danger collapse'
        style={{ textAlign : 'center' }} id='balChangeError'>
          You must enter a number
        </p>
        <p className='border border-danger rounded p-2 text-danger collapse'
        style={{ textAlign : 'center' }} id='reasonError'>
          You must enter a reason
        </p>
        <div className='input-group'>

          <div className='input-group-prepend mb-3'>
            <span className='input-group-text'>Amount: $</span>
          </div>
          <input type="number" className='form-control' name="username" autoFocus="" id="amount" />
        </div>
        <div className='input-group'>
          <div className='input-group-prepend'>
            <span className='input-group-text'>Reason:</span>
          </div>
          <input type="text" className='form-control' name="username" autoFocus="" id="reason" />
        </div>
      </form>
    );
    for (var child in this.state){
      let childInfo = {
        username : child,
        childName : this.state[child].firstName,
        childNum : i,
        balance : this.state[child].balance
      };
      childInfoElements.push(<ChildInfo info={ childInfo } key={ i.toString() }
      onClick={ () => this.setCurrChild(childInfo.username) }
      histClick={ () => this.buildHistTable(childInfo.username) }/>);
      i++;
    }
    return (
      <div className="accordion" id="childrenAccounts" style={{ width: '60%', margin: 'auto' }}>
        <AllowanceModal modalname='WD' header='' modalbody={ WDModalBody }
        onClick={ () => this.changeBalance() }/>
        <AllowanceModal modalname='hist' header='History' modalbody={ histModalBody } size='modal-lg'/>
        { childInfoElements }
      </div>
    );
  }
}

class ParentHome extends React.Component {
  constructor(props){
    super(props);
  }

  render (){

    return (
      <div>
        <ParentModals />
        <ParentNavBar />
        <Welcome />
        <Children />
      </div>
    );
  }
};

let parentRoot = document.getElementById('parent');
ReactDOM.render(
  <ParentHome />,
  parentRoot
);

$('#WDModal').on('show.bs.modal', function(event) {
  $('#WDLabel').html($(event.relatedTarget).html());
});
