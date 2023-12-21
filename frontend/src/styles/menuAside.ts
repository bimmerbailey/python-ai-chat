import { mdiAccountCircle, mdiMonitor , mdiChat} from '@mdi/js'

interface AsideMenu {
  to: string
  label: string
  icon: string
}

export default <Array<AsideMenu>> [
  {
    to: '/',
    icon: mdiMonitor,
    label: 'Dashboard',
  },
  {
    to: '/profile',
    label: 'Profile',
    icon: mdiAccountCircle,
  },
  {
    to: '/users',
    label: 'Users',
    icon: mdiAccountCircle,
  },
  {
    to: '/chat',
    label: 'Chat',
    icon: mdiChat,
  },
]
