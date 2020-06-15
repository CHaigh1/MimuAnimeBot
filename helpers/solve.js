var solve = function solve(num1, sign, num2){
  switch(sign){
    case '+':
      return num1 + num2;
    break;

    case '-':
      return num1 - num2;
    break;

    case '*':
      return num1 * num2;
    break;

    case 'x':
      return num1 * num2;
    break;

    case '/':
      return num1 / num2;
    break;

    default:
      return 'not a valid sign';
    break;
  }
}

module.exports.solve = solve;