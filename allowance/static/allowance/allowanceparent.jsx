function Modals(props){
  return (
    <div>
      <AllowanceModal modalname='addChild' header='Add Child'/>
      <AllowanceModal modalname='removeChild' header='Remove Child'/>
      <AllowanceModal modalname='prCode' header='Parent Registration Code' />
      <AllowanceModal modalname='changePW' header='Change Password' />
    </div>
  );
}

function NavElement(props) {
  return (
    <li
      className='nav-item nav-link'
      data-toggle='modal'
      data-target={ props.modallabel }
      style={{ cursor: 'pointer' }}
    >
      { props.itemlabel }
    </li>
  );
}

function ParentNavBar(props) {
  let link = $('#parent').data('link');
  return (
    <nav className='navbar navbar-expand navbar-light bg-info' style={{ fontWeight: 'bold' }}>
      <ul className='navbar-nav mr-auto'>
        <NavElement modallabel='#addChildModal' itemlabel='Add Child' />
        <NavElement modallabel='#removeChildModal' itemlabel='Remove Child' />
        <NavElement modallabel='#prCodeModal' itemlabel='Parent Registration Code' />
        <NavElement modallabel='#changePWModal' itemlabel='Change Password' />
      </ul>
      <ul className='navbar-nav'>
        <li className='nav-item'>
          <a className='nav-link' href={ link }>Logout</a>
        </li>
      </ul>
    </nav>
  );
}

function Welcome(props) {
  let parentName = $('#parent').data('user').firstName;
  return (
    <h2 style={{ textAlign : 'center' }}>Welcome { parentName }</h2>
  );
}

function ChildInfo(props) {
  let target = "collapse" + props.childnum;
  let name = props.childname;
  let heading = "heading" + props.childnum;
  return (
    <div className="card">
      <div className="card-header p-0" id={ heading }>
        <h2 className="mb-0">
          <button className="btn btn-info btn-lg btn-block mb-0 shadow-none collapsed" 
                  type="button" data-toggle="collapse" data-target={ "#" + target } 
                  aria-expanded="false" aria-controls={ target }>
            { name }
          </button>
        </h2>
      </div>

      <div id={ target } className="collapse" aria-labelledby={ heading } data-parent="#childrenAccounts">
        <div className="card-body">
          PlaceHolder
        </div>
      </div>
    </div>
  );
}

function Children(props) {
  let children = $('#parent').data('children');
  let childInfoElements = [];
  let i = 1;
  for (var child in children){
    let name = children[child].firstName;
    childInfoElements.push(<ChildInfo childname={ name } childnum={ i } key={ i.toString() }/>);
    i++;
  }
  return (
    <div className="accordion" id="childrenAccounts" style={{ width: '60%', margin: 'auto' }}>
      { childInfoElements }
    </div>
  );
}

class ParentHome extends React.Component {
  constructor(props){
    super(props);
  }
  
  render (){
    
    return (
      <div>
        <Modals />
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
