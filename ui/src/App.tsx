import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { Layout, Menu } from 'antd';
import routes from '../src/components/Routes';
import './App.css';

const { Header, Content, Footer } = Layout;

const App: React.FC = () => (
    <Router>
      <MainLayout />
    </Router>
);

const MainLayout: React.FC = () => {
  const location = useLocation();
  const selectedKey = routes.find(route => route.path === location.pathname)?.key || 'home';

  return (
      <Layout className="layout">
        <Header>
          <div className="logo" />
          <Menu theme="dark" mode="horizontal" selectedKeys={[selectedKey]}>
            {routes.map(route => (
                <Menu.Item key={route.key}>
                  <Link to={route.path}>{route.label}</Link>
                </Menu.Item>
            ))}
          </Menu>
        </Header>
        <Content style={{ padding: '0 50px' }}>
          <div className="site-layout-content" style={{'height': '80vw'}}>
            <Routes>
              {routes.map(route => (
                  <Route key={route.key} path={route.path} element={<route.Component />} />
              ))}
            </Routes>
          </div>
        </Content>
        {/*<Footer style={{ textAlign: 'center' }}>Ant Design ©2023 Created by Ant UED</Footer>*/}
      </Layout>
  );
};

export default App;
