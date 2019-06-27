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
  let childName = $('#parent').data('user').firstName;
  return (
    <h2 style={{ textAlign : 'center' }}>Welcome { childName }</h2>
  );
}

function ChildHist(props){
  let uname = $('#child').data('user').userName;
  return (
    <div>
      <AllowanceHistTable child={uname} />
    </div>
  )
}

function ChildHome(props){
  return (
    <ChildNavBar />,
    <Welcome />,
    <ChildHist />
  );
}
ReactDOM.render(<ChildHome />, document.getElementById('child'));