// JavaScript source code
var rad = .05;
AFRAME.registerPrimitive('a-tcyl', {
    defaultComponents: {
        geometry: {
            primitive: 'cylinder',
            radius: rad
        },
        material: {},
        clickablecyl: {}
    },
    mappings: {
        radius: 'geometry.radius',
        color: 'material.color',
        height: 'geometry.height',
        opos: 'position',
        filter: 'clickablecyl.filter'
    }
});

AFRAME.registerPrimitive('a-txt', {
    defaultComponents: {
        text: {
            width: 3,
            align: 'center',
            color: 'pink',
            side: 'double'
        }
    },
    mappings: {
        value: 'text.value'
    }
});

AFRAME.registerPrimitive('a-parabola', {
    defaultComponents: {
        geometry: {
            primitive: 'parabola'
        },
        material: {
            side: 'double'
        }
    },
    mappings: {
        top: 'geometry.top',
        bot: 'geometry.bot',
        start: 'geometry.start',
        end: 'geometry.end',
        segments: 'geometry.segments',
        color: 'material.color'
    }
});

AFRAME.registerGeometry('parabola', {
    schema: {
        top: { type: 'number', default: 2 },
        bot: { type: 'number', default: 1 },
        start: { type: 'string', default: '-2 0 0' },
        end: { type: 'string', default: '2 0 0' },
        segments: { type: 'int', default: 49 }
    },

    init: function (data) {
        var geometry = new THREE.Geometry();
        geometry.vertices = points(data.start, data.end, data.segments, data.top, data.bot);
        geometry.computeBoundingBox();

        geometry.faces.push(new THREE.Face3(0, data.segments, 1));
        var topi = 1;
        var boti = data.segments;
        i = 1;
        while (topi < data.segments - 1) {
            if (i % 2 == 1) {
                geometry.faces.push(new THREE.Face3(topi, boti, boti + 1));
            }
            else {
                geometry.faces.push(new THREE.Face3(topi, boti + 1, topi + 1));
                boti++;
                topi++;
            }
            i++;
        }
        geometry.faces.push(new THREE.Face3(topi, boti, geometry.vertices.length-1));
        geometry.mergeVertices();
        geometry.computeFaceNormals();
        geometry.computeVertexNormals();
        this.geometry = geometry;
    }
});

function points(startPos, endPos, segments, top, bot) {
    var arr = [];
    var sp = new THREE.Vector3()
        .fromArray(startPos.split(' ')
            .map(function (coord) {
                return parseFloat(coord);
            })
        );
    var ep = new THREE.Vector3()
        .fromArray(endPos.split(' ')
            .map(function (coord) {
                return parseFloat(coord);
            })
        );
    arr.push(sp);
    var len = sp.distanceTo(ep);
    var incr = len / segments;
    var zincr = (ep.z - sp.z) / len * incr;
    var xincr = (ep.x - sp.x) / len * incr;
    var ht = len * len / 4;
    var hratio = top / ht;
    for (yx = -len / 2 + incr, x = sp.x + xincr, z = sp.z + zincr; yx < len / 2; yx += incr, x += xincr, z += zincr) {
        y = (ht - yx * yx)*hratio;
        arr.push(new THREE.Vector3(x, y, z));
    }
    if (bot) {
        hratio = bot / ht;
    }
    else {
        hratio = 0;
    }
    for (yx = -len / 2 + incr, x = sp.x + xincr, z = sp.z + zincr; yx <= len / 2; yx += incr, x += xincr, z += zincr) {
        y = (ht - yx * yx) * hratio;
        arr.push(new THREE.Vector3(x, y, z));
    }
    arr.push(ep);
    return arr;
}
