// JavaScript source code
var filters = '';
AFRAME.registerComponent('clickablecyl', {
    schema : {
        filter: { type: 'string', default: '_dfilter' },
        clicked: { type: 'boolean', default: false }
    },
    init: function () {
        this.el.addEventListener('click', function (event) {
            elrc = event.detail.cursorEl.getAttribute('raycaster');
            rc = new THREE.Raycaster(elrc.origin, elrc.direction, elrc.near, elrc.far);
            cyls = document.getElementsByTagName('a-tcyl');
            mindist = rc.intersectObject(this.object3D, true)[0].distance;
            var minindex;
            for (var i = 0; i < 21; i++){
                var arr = rc.intersectObject(cyls[i].object3D, true);
                if (arr.length && arr[0].distance <= mindist) {
                    minindex = i;
                    mindist = arr[0].distance;
                }
            }
            clickobj = cyls[minindex].getAttribute('clickablecyl');
            if (clickobj.clicked) {
                filters = filters.replace('_'+clickobj.filter, '');
            }
            else {
                filters += '_'+clickobj.filter;
            }
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4) {
                    var json = JSON.parse(this.responseText);
                    //adjust cylinders
                    for (id in json['cyls']) {
                        var ele = document.getElementById(id)
                        if (json['cyls'][id][0] == 0) {
                            //use small number because 0 defaults to 1
                            ele.setAttribute('height', 0.000001);
                            ele.setAttribute('visible', false);
                            ele.object3D.position.y = 0;
                        }
                        else {
                            ele.setAttribute('height', json['cyls'][id][0]);
                            ele.setAttribute('visible', true);
                            ele.object3D.position.y = json['cyls'][id][1];
                        }
                    }
                    //adjust cylinder labels
                    for (id in json['text']) {
                        var ele = document.getElementById(id);
                        ele.object3D.position.y = json['text'][id];
                    }
                    //adjust parabolas
                    for (id in json['parab']) {
                      var ele = document.getElementById(id);
                      ele.setAttribute('top', json['parab'][id][0]);
                      if (json['parab'][id][1] != 0) {
                        ele.setAttribute('bot', json['parab'][json['parab'][id][1]][0]);
                      }
                    }
                    //display applied filters
                    ele = document.getElementById('filters');
                    while (ele.children[1]) {
                        ele.removeChild(ele.children[1]);
                    }
                    if (filters) {
                        fltrList = filters.split('_');
                        for (i in fltrList) {
                            if (fltrList[i]){
                               li = document.createElement('li');
                               li.classList.add('list-group-item');
                               li.innerHTML=fltrList[i];
                               ele.appendChild(li);
                            }
                        }
                    }
                    else {
                      li = document.createElement('li');
                      li.classList.add('list-group-item');
                      li.innerHTML="None";
                      ele.appendChild(li);
                    }
                }
            }
            xhttp.open('GET', 'fltrs/?q=' + filters, true);
            xhttp.send();
            var elements = document.getElementsByTagName('a-tcyl');
            for (var i = 0; i < elements.length; i++) {
                var ele = elements[i].getAttribute('clickablecyl');
                if ( ele.filter == clickobj.filter) {
                    ele.clicked = !ele.clicked;
                }
            }

            /*
            var vis = event.currentTarget.getAttribute('visible');
            if (vis) {
                var mat = event.currentTarget.getAttribute('material');
                var testEvent = new CustomEvent('cylclicked', {
                    detail: {
                        color: mat.color
                    }
                });
                var cyls = document.getElementsByTagName('a-tcyl');
                for (var i = 0; i < cyls.length; i++) {
                    cyls[i].dispatchEvent(testEvent);
                }
            }
            */
        });
    }
});
/*
AFRAME.registerComponent('cyllistener', {
    schema: {
        opos: { type: 'string', default: '0 0 0' },
        clicked: { type: 'boolean', default: false}
    },
    init: function () {
        var ele = this.el;
        //console.log(ele.object3D);
        var cll = ele.getAttribute('cyllistener')
        var parts = cll.opos.split(' ');
        cll.orig = {
            x: parseFloat(parts[0]),
            y: parseFloat(parts[1]),
            z: parseFloat(parts[2]),
            height: ele.getAttribute('height')
        }
        ele.object3D.position.set(cll.orig.x, cll.orig.y, cll.orig.z);
        this.el.addEventListener('cylclicked', function (event) {
            if (ele.getAttribute('material').color == event.detail.color) {
                if (cll.clicked) {
                    ele.object3D.position.set(cll.orig.x, cll.orig.y, cll.orig.z);
                    cll.clicked = false;
                }
                else {
                    ele.object3D.position.set(cll.orig.x, cll.orig.height/2, cll.orig.z);
                    cll.clicked = true;
                }
            }
            else {
                if (ele.getAttribute('visible')) {
                    ele.object3D.position.y = -cll.orig.height * 2;
                    ele.setAttribute('visible', false);
                }
                else {
                    ele.object3D.position.y = cll.orig.y;
                    ele.setAttribute('visible', true);
                }
            }
        });
    }
});
*/
