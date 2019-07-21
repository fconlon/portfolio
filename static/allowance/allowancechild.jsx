function ChildNavBar(props){
  let navBody = (
    <div>
      <ul className='navbar-nav ml-auto'>
        <li className='nav-item'>
          <a className='nav-link' href='/allowance/logout?next=/allowance/login'>Logout</a>
        </li>
      </ul>
    </div>
  );
  let classes = 'navbar-light bg-info';
  return (
    <AllowanceNavBar classes={ classes } body={ navBody } />
  );
}

function Welcome(props) {
  let childName = $('#child').data('user').firstName;
  return (
    <h2 style={{ textAlign : 'center' }}>Welcome { childName }</h2>
  );
}

class ChildHist extends React.Component{
  constructor(props){
    super(props);
  }

  componentDidMount(){
    $.get('/allowance/childbalance', function(data){
      $("#childBalance").html("$" + data.balance);
    });
  }

  render(){
    let uname = $('#child').data('user').userName;
    let navBody = (
      <div>
        <ul className="navbar-nav mr-auto">
          <li className="navbar-item">Balance</li>
        </ul>
        <ul className="navbar-nav">
          <li className="navbar-item" id="childBalance"></li>
        </ul>
      </div>
    )
    return (
      <div className='list-group' style={{ width: '60%', margin: 'auto' }}>
        <div className="list-group-item bg-info" style={{ textAlign: 'center', fontWeight: 'bold'}}>
          Account Information
        </div>
        <div className="list-group-item">
          <AllowanceNavBar body={ navBody }/>
        </div>
        <div className="list-group-item">
          <AllowanceHistTable child={uname} />
        </div>
      </div>
    )
  }
}

function ChildHome(props){
  return (
    <div>
      <ChildNavBar />,
      <Welcome />,
      <ChildHist />
    </div>
  );
}
ReactDOM.render(<ChildHome />, document.getElementById('child'));