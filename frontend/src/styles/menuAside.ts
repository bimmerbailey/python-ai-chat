import { mdiAccountCircle, mdiMonitor , mdiChat} from '@mdi/js'

export default [
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
