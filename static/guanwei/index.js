/**
 ** On ready
 */
document.onreadystatechange = function subSomething() {
  if (document.readyState === 'complete') {
    var loadingElement = document.getElementById('loading');
    if (!loadingElement) return;
    loadingElement.style.opacity = 0;
    setTimeout(function () {
      loadingElement.style.display = 'none';
    }, 300);
  }
};

/**
 ** Init swiper
 */
var mySwiper = new Swiper('.swiper-container', {
  direction: 'vertical',
  pagination: {
    el: '.swiper-pagination',
  },
  on: {
    init: function () {
      swiperAnimateCache(this); //隐藏动画元素
      swiperAnimate(this); //初始化完成开始动画
    },
    slideChangeTransitionEnd: function () {
      swiperAnimate(this); //每个slide切换结束时也运行当前slide动画
      //this.slides.eq(this.activeIndex).find('.ani').removeClass('ani'); 动画只展现一次，去除ani类名
    },
  },
});
