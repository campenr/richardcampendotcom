module.exports = {
  mode: 'jit',
  theme: {
    fontFamily: {
      'sans': ['Libre Franklin', 'sans-serif'],
    },
    colors: {
      'blue': '#007BFF',
      'grey-50': '#F9FAFB',
      'black-muted': '#212529',
      'gree': '#c1d56a',
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