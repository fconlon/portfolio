function AllowanceModal(props) {
  let modalID = props.modalname + "Modal";
  let modalLabel = props.modalname + "Label";
  return (
    <div className="modal fade" id={ modalID } tabindex="-1" role="dialog" 
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
            ...
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" data-dismiss="modal">Close</button>
            <button type="button" className="btn btn-primary">Save changes</button>
          </div>
        </div>
      </div>
    </div>
  );
}