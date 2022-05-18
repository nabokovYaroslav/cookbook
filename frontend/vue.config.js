const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  runtimeCompiler: true,
  configureWebpack: {
    watchOptions: {
      ignored: /node_modules/,
      poll: 1000,
    },
  },
  transpileDependencies: true,
});
