<template>
  <div class="recipe">
    <div class="image">
      <span class="category">
        <router-link
          :to="{ name: 'category', params: { id: recipe.category } }"
          >{{ recipe.category_name }}</router-link
        >
      </span>
      <router-link
        :to="{
          name: 'recipe',
          params: { category_id: recipe.category, id: recipe.id },
        }"
      >
        <img
          :src="recipe.image.url"
          :srcset="recipe.image.srcset"
          sizes="(max-width: 576px) 540px,
                           (max-width: 768px) 720px,
                           (max-width: 992px) 960px,
                           1140px
                           "
          alt="recipe"
        />
      </router-link>
    </div>
    <div class="caption">
      <router-link
        :to="{
          name: 'recipe',
          params: { category_id: recipe.category, id: recipe.id },
        }"
        >{{ recipe.name }}</router-link
      >
    </div>
    <div class="meta">
      <div class="meta-left">
        <span class="time">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            class="bi bi-clock"
            viewBox="0 0 16 16"
          >
            <path
              d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"
            />
            <path
              d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"
            />
          </svg>
          <span>{{ recipe.time }} мин.</span>
        </span>
        <span class="serves">
          <svg
            version="1.0"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 834.000000 1280.000000"
            preserveAspectRatio="xMidYMid meet"
          >
            <g
              transform="translate(0.000000,1280.000000) scale(0.100000,-0.100000)"
              stroke="none"
            >
              <path
                d="M575 12786 c-42 -18 -107 -94 -140 -164 -128 -268 -203 -781 -245
-1667 -20 -429 -28 -1426 -19 -2585 4 -635 11 -1200 14 -1255 15 -243 44 -407
129 -745 74 -293 80 -349 72 -735 -23 -1113 -79 -1808 -241 -3015 -110 -814
-132 -1020 -141 -1325 -10 -317 19 -585 91 -836 45 -156 73 -208 160 -294 111
-111 221 -157 380 -158 154 -2 299 55 401 157 105 105 148 224 196 531 17 115
21 185 21 390 1 286 -9 406 -84 1000 -116 928 -154 1290 -194 1855 -34 494
-65 1365 -65 1830 0 268 10 302 211 738 208 451 282 651 342 922 66 294 78
488 66 1067 -36 1839 -253 3390 -560 3993 -120 237 -271 350 -394 296z"
              />
              <path
                d="M6865 12734 c-88 -21 -118 -31 -176 -60 -508 -252 -958 -1308 -1073
-2514 -60 -625 -39 -1043 69 -1368 118 -353 285 -569 685 -887 214 -170 254
-210 287 -282 l26 -56 -7 -426 c-22 -1368 -73 -2168 -246 -3851 -81 -794 -95
-935 -114 -1215 -43 -608 -27 -1031 55 -1436 48 -238 97 -358 190 -462 100
-113 221 -169 364 -170 235 -2 429 148 515 398 22 63 53 227 74 390 28 208 39
480 33 765 -10 417 -28 664 -127 1755 -144 1582 -189 2359 -211 3613 -12 756
-19 704 100 822 44 43 141 120 230 180 403 275 583 494 700 850 79 242 96 383
95 775 -1 716 -102 1371 -299 1935 -231 660 -567 1099 -934 1219 -62 20 -196
35 -236 25z"
              />
              <path
                d="M3072 12717 c-61 -73 -130 -554 -186 -1302 -76 -996 -102 -2176 -56
-2521 31 -241 113 -420 297 -653 261 -328 328 -437 375 -606 19 -70 22 -104
21 -265 0 -102 -8 -266 -17 -365 -9 -99 -48 -508 -86 -910 -199 -2090 -254
-2908 -267 -3935 -10 -896 41 -1536 146 -1805 129 -332 462 -451 750 -268 158
101 239 249 290 533 59 327 75 572 68 1020 -8 441 -17 560 -117 1570 -130
1307 -172 1870 -210 2825 -18 459 -30 1381 -19 1488 19 187 70 290 249 507
287 348 402 597 440 955 18 164 24 811 11 1175 -29 840 -108 1849 -182 2335
-64 422 -92 281 -124 -615 -37 -1071 -48 -1298 -71 -1570 -31 -370 -68 -536
-117 -517 -28 10 -47 63 -66 184 -38 233 -54 557 -76 1523 -15 673 -27 963
-45 1103 -23 181 -58 160 -79 -48 -11 -102 -32 -622 -51 -1255 -32 -1066 -77
-1473 -167 -1507 -27 -10 -60 40 -78 119 -49 212 -63 500 -75 1478 -13 1057
-26 1335 -65 1335 -41 0 -71 -326 -105 -1150 -57 -1371 -100 -1785 -185 -1785
-36 0 -74 147 -95 360 -25 270 -36 614 -50 1665 -9 628 -19 867 -39 903 -6 11
-9 11 -19 -1z"
              />
            </g>
          </svg>
          <span>{{ recipe.count }}</span>
        </span>
      </div>
      <div class="meta-right">
        <span class="comments">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            class="bi bi-chat"
            viewBox="0 0 16 16"
          >
            <path
              d="M2.678 11.894a1 1 0 0 1 .287.801 10.97 10.97 0 0 1-.398 2c1.395-.323 2.247-.697 2.634-.893a1 1 0 0 1 .71-.074A8.06 8.06 0 0 0 8 14c3.996 0 7-2.807 7-6 0-3.192-3.004-6-7-6S1 4.808 1 8c0 1.468.617 2.83 1.678 3.894zm-.493 3.905a21.682 21.682 0 0 1-.713.129c-.2.032-.352-.176-.273-.362a9.68 9.68 0 0 0 .244-.637l.003-.01c.248-.72.45-1.548.524-2.319C.743 11.37 0 9.76 0 8c0-3.866 3.582-7 8-7s8 3.134 8 7-3.582 7-8 7a9.06 9.06 0 0 1-2.347-.306c-.52.263-1.639.742-3.468 1.105z"
            />
          </svg>
          <span>{{ recipe.comments_count }}</span>
        </span>
        <span class="meta-views">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            class="bi bi-eye"
            viewBox="0 0 16 16"
          >
            <path
              d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"
            />
            <path
              d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"
            />
          </svg>
          <span>{{ recipe.views_count }}</span>
        </span>
      </div>
    </div>
    <div class="description">{{ recipe.description }}</div>
  </div>
</template>

<script>
export default {
  props: {
    recipe: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
.recipe {
  margin-bottom: 48px;
}

.recipe svg {
  width: 16px;
  height: 16px;
  fill: #ff4e00;
}

.recipe .image {
  position: relative;
  overflow: hidden;
}

.recipe .image .category a {
  position: absolute;
  left: 0.8rem;
  bottom: 0.5rem;
  font-size: 0.7em;
  transform: translateY(5em) translateZ(0);
  transition: all 0.3s;
  z-index: 3;
  padding: 2px 9px;
  background: #ff4e00;
  color: #fff;
  border-radius: 3px;
  text-decoration: none;
  font-size: 0.7em;
}

.recipe:hover .image .category a {
  transform: translateY(0) translateZ(0);
}

.recipe .image .category a:hover {
  background-color: #222;
}

.recipe .image > a {
  width: 100%;
  height: 150px;
  display: block;
}

.recipe .image > a img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 6px;
}

.recipe .caption {
  color: #222;
  font-weight: 700;
  font-size: 16px;
  line-height: 19.2px;
  margin-top: 12px;
}

.recipe .meta {
  margin-top: 12px;
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
}

.recipe .meta > * {
  margin-left: -24px;
  display: flex;
  margin-bottom: 12px;
}

.recipe .meta > * > * {
  margin-left: 24px;
  display: flex;
  align-items: center;
}

.recipe .meta > * > * > span {
  margin-left: 6px;
  color: #666;
  font-size: 12.8px;
}

.recipe .description {
  margin-top: 12px;
  font-size: 0.9em;
  line-height: 1.4;
  color: #666;
}
</style>
