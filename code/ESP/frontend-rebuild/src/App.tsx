import { Header } from 'components/Header';
import { Footer } from 'components/Footer';
import { ToastNotificationContainer } from 'components/ToastNotifications';
import { Container } from 'components/primitives/Layout';
// import { GuildsPage } from './Modules/Guilds/pages/Guilds';

import GlobalStyle from './theme/GlobalTheme';

// import { GuildsContextProvider, TransactionsProvider } from 'contexts/Guilds';

// import { LandingPage } from 'Modules/Guilds/pages/LandingPage';
import NotFound from './pages/NotFound';
import { Route, Routes } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import { GuildsDarkTheme } from './components/theme';

import { OnlineStatus } from 'components/OnlineStatus';


const App = () => {
  return (
    <ThemeProvider theme={GuildsDarkTheme}>
      <GlobalStyle />

      {/* <TransactionsProvider> */}
        <Header />

        {/* <GuildsContextProvider> */}
          <Container>
            <OnlineStatus>
              <Routes>
                {/* <Route path="/:chainName" element={<LandingPage />} />
                <Route path="/:chainName/:guildId" element={<GuildsPage />} /> */}
                <Route path="*" element={<NotFound />} />
              </Routes>
            </OnlineStatus>
          </Container>
          <Footer />
        {/* </GuildsContextProvider> */}
      {/* </TransactionsProvider> */}

      <ToastNotificationContainer autoClose={10000} limit={4} />
    </ThemeProvider>
  );
};

export default App;
