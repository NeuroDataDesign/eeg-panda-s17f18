function rotate(e){
  if(e.data.d==="n"){
    e.data.car.currdeg = e.data.car.currdeg - 72;
  }
  if(e.data.d==="p"){
    e.data.car.currdeg = e.data.car.currdeg + 72;
  }
  e.data.car.css({
    "-webkit-transform": "rotateY("+e.data.car.currdeg+"deg)",
    "-moz-transform": "rotateY("+e.data.car.currdeg+"deg)",
    "-o-transform": "rotateY("+e.data.car.currdeg+"deg)",
    "transform": "rotateY("+e.data.car.currdeg+"deg)"
  });
}

var carousel = $(".carousel-norm");
carousel.currdeg  = 0;

$(".next-norm").on("click", { d: "n", car: carousel}, rotate);
$(".prev-norm").on("click", { d: "p", car: carousel }, rotate);

var embed_carousel = $(".carousel-embed");
embed_carousel.currdeg  = 0;

$(".next-embed").on("click", { d: "n", car: embed_carousel}, rotate);
$(".prev-embed").on("click", { d: "p", car: embed_carousel }, rotate);

var cluster_carousel = $(".carousel-clust");
cluster_carousel.currdeg  = 0;

$(".next-clust").on("click", { d: "n", car: cluster_carousel}, rotate);
$(".prev-clust").on("click", { d: "p", car: cluster_carousel }, rotate);
