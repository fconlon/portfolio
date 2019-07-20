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
  let classes = 'navbar-dark bg-info';
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

function ChildHist(props){
  let uname = $('#child').data('user').userName;
  //let balance;
  //$.post()
  return (
    <div className='list-group' style={{ width: '60%', margin: 'auto' }}>
      <div className="list-group-item bg-info" style={{ textAlign: 'center'}}>
        Account Information
      </div>
      <div className="list-group-item">
        <AllowanceHistTable child={uname} />
      </div>
      
    </div>
  )
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