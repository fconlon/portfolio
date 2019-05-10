function AllowanceModal(props) {
  let modalID = props.modalname + "Modal";
  let modalLabel = props.modalname + "Label";
  let modalBody = props.modalbody;
  
  return (
    <div className="modal fade" id={ modalID } tabIndex="-1" role="dialog" 
    aria-labelledby={ modalLabel } aria-hidden="true">
      <div className="modal-dialog modal-dialog-centered" role="document">
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

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}