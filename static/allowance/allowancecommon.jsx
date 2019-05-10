var rows = [];
function AllowanceModal(props) {
  let modalID = props.modalname + "Modal";
  let modalLabel = props.modalname + "Label";
  let modalBody = props.modalbody;
  let modalDialog = "modal-dialog modal-dialog-centered " + props.size;
  
  return (
    <div className="modal fade" id={ modalID } tabIndex="-1" role="dialog" 
    aria-labelledby={ modalLabel } aria-hidden="true">
      <div className={ modalDialog } role="document">
        <div className="modal-content">
          <div className="modal-header bg-info">
            <h5 className="modal-title text-white" id={ modalLabel }>{ props.header }</h5>
            <button type="button" className="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div className="modal-body">
            { modalBody }
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" data-dismiss="modal" >Close</button>
            <button type="button" className="btn btn-primary" onClick={ props.onClick }>Save changes</button>
          </div>
        </div>
      </div>
    </div>
  );
}

function NavModalTrigger(props) {
  return (
    <li
      className='nav-item nav-link'
      data-toggle='modal'
      data-target={ props.modallabel }
      style={{ cursor: 'pointer' }}
      onClick={ props.onClick }
    >
      { props.itemlabel }
    </li>
  );
}

function AllowanceNavBar(props) {
  let classes = 'navbar navbar-expand-sm ' + props.classes;
  return (
    <nav className={ classes } style={{ fontWeight: 'bold' }}>
      { props.body.props.children }
    </nav>
  );
}

class AllowanceHistTable extends React.Component{
  constructor(props){
    super(props);
    this.rows = [];
    this.state = { child: this.props.child };
  }
  
  buildTable(uname){
    this.setState({ child: uname });
  }
  
  responseHandler(data, status, xhttp){
    rows = [];
    for(var key in data){
      let row = (
        <tr key={ key }>
          <td>{ data[key].reason }</td>
          <td>{ data[key].date }</td>
          <td>{ data[key].transation }</td>
        </tr>
      );
      rows.push(row);
    }
  }
  
  render() {
    $.ajax({
      type: 'POST',
      url: '/allowance/childhistory/',
      data: { username: this.state.child },
      success: this.responseHandler,
      dataType: 'json',
      async: false
    });
    return (
      <table id='hist' className='table table-striped table-bordered'>
        <thead>
          <tr>
            <th>Reason</th>
            <th>Date</th>
            <th>Change</th>
          </tr>
        </thead>
        <tbody>
          { rows }
        </tbody>
      </table>
    );
  }
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    let csrftoken = $('meta[name="csrf-token"]').prevObject[0].cookie.split('=')[1];
    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});