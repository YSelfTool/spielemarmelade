
function load(name) {
    var img = new Image();
    img.src = "gfx/" + name + ".png";
    return img;
}

function ImageLoader() {
    this.images = new Object();
}
ImageLoader.prototype.load = function(name) {
    this.images[name] = load(name);
};
ImageLoader.prototype.get = function(name) {
    if (!(name in this.images)) {
        this.load(name);
    }
    return this.images[name];
};

function preloadImages(imgloader) {
    imgloader.load("tile-red");
    imgloader.load("tile-green");
    imgloader.load("tile-blue");
    imgloader.load("tile-purple");
    imgloader.load("tile-yellow");
    imgloader.load("tile-turquoise");
    imgloader.load("tile-brown");
    imgloader.load("unit-1");
    imgloader.load("unit-0");
}
