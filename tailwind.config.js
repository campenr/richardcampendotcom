module.exports = {
  mode: 'jit',
  theme: {
    fontFamily: {
      'sans': ['Libre Franklin', 'sans-serif'],
    },
    colors: {
      'blue': '#006FEA',
      'grey': '#F9FAFB',
      'black-muted': '#212529',
    },
    extend: {
      screens: {
        xs: '480px',
      }
    }
  },
  purge: {
    content: ['./app/app/**/*.html'],
  },
}