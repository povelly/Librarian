import Search from "./components/Search";
import NavigationBar from "./components/NavigationBar";

// css pour react-bootstrap
import 'bootstrap/dist/css/bootstrap.min.css';
// css global de la webapp
import "./style/global.css";


function App() {
  return (
    <div className="App">
      <NavigationBar/>
      <Search />
    </div>
  );
}

export default App;
