// JavaScript source code
AFRAME.registerComponent('clickablecyl', {
    init: function () {
        this.el.addEventListener('click', function (event) {
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
        });
    }
});

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